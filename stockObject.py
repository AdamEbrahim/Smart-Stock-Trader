from enum import Enum
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import MarketMoversRequest, StockLatestQuoteRequest, StockQuotesRequest, StockLatestTradeRequest, StockTradesRequest, StockBarsRequest, StockLatestBarRequest
import threading
from collections import deque
from datetime import datetime, timedelta, timezone
from utilities import isMarketOpen, isMarketOpenDay, getLastClose

#UI stuff
import tkinter as tk

import matplotlib
matplotlib.use('agg')
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

#style.use("ggplot")

class dataType(Enum):
    BAR = "Bar"
    TRADE = "Trade"
    QUOTE = "Quote"


class stockObject:

    #timeframeUnit is an enum alpaca.data.timeframe.TimeFrameUnit, "oneYear" for year interval, or "fiveYear" for five year interval
    def __init__(self, api_key, secret_key, symbol, timeframeUnit, parentUI):
        self.api_key = api_key
        self.secret_key = secret_key
        self.symbol = symbol

        self.model = dataType.TRADE
        
        #need a lock for data as web socket thread and main thread (when initializing historical data) may write to data at same time
        self.data = deque() #probably show previous close at each data point
        self.dataLock = threading.Lock()
        self.maxDataPoints = 60

        self.currentPrice = 0

        self.timeInterval = timeframeUnit

        self.hasUpdatedLastMinute = False

        self.initHistoricData()

        #stock tkinter UI object
        self.stockUI = singleStockUI(parentUI, self.data)


    #timeframeUnit is an enum alpaca.data.timeframe.TimeFrameUnit
    def changeTimeInterval(self, timeframeUnit):
        self.timeInterval = timeframeUnit
        print("changed time interval")
        self.initHistoricData()

        self.stockUI.changeContents(self.data) #make sure to show updated data in stock UI plot


    def initHistoricData(self):
        client = StockHistoricalDataClient(self.api_key, self.secret_key)
        requiredTimeFrame = 0
        requiredStart = 0
        now = datetime.now(timezone.utc)

        #if market closed right now, get last close to use as the end time of retrieving historical data
        if not isMarketOpen(now):
            now = getLastClose(now)

        match self.timeInterval:
            case TimeFrameUnit.Minute: #live data feed
                print("Minute")

            case TimeFrameUnit.Hour: #show last 1 hour (maybe 3?)
                print("Hour")
                d = timedelta(hours=1)
                requiredStart = now - d

                requiredTimeFrame = TimeFrame.Minute

            case TimeFrameUnit.Day: #show since beginning of day
                print("Day")
                requiredStart = now.date()

                requiredTimeFrame = TimeFrame(5, TimeFrameUnit.Minute) #every 5 minutes

            case TimeFrameUnit.Week: #show since beginning of day 1 week ago
                print("Week")
                d = timedelta(weeks=1)
                requiredStart = now - d
                requiredStart = requiredStart.date()

                requiredTimeFrame = TimeFrame.Hour

            case TimeFrameUnit.Month: #show since beginning of day 1 month ago
                print("Month")
                d = timedelta(days=31)
                requiredStart = now - d
                requiredStart = requiredStart.date()

                requiredTimeFrame = TimeFrame.Day

            case "oneYear": #show since beginning of day 1 year ago
                print("1 Year")
                d = timedelta(days=365)
                requiredStart = now - d
                requiredStart = requiredStart.date()

                requiredTimeFrame = TimeFrame.Day 

            case _: #show since beginning of day 5 year ago
                print("5 year")
                d = timedelta(days=365*5)
                requiredStart = now - d
                requiredStart = requiredStart.date()

                requiredTimeFrame = TimeFrame.Week
        

        print(requiredStart)
        #endtime defaults to now
        barsRequest = StockBarsRequest(symbol_or_symbols=self.symbol, timeframe=requiredTimeFrame, start=requiredStart)
        bars = client.get_stock_bars(barsRequest)
        barData = bars[self.symbol]

        # if len(barData) < self.maxDataPoints:
        #     #todo: implement feature for what to do with less than maxdatapoints like if it is still morning
        #     print("error in retrieving stock data; insufficient number of data points")
        #     return
        
        # interval = (1.0 * (len(barData) - 1)) / (self.maxDataPoints - 1)

        self.dataLock.acquire()
        print("hi")
        self.data.clear()

        i = 0
        while i < len(barData):
            print(i)
            self.data.append({"close": barData[int(i)].close,
                              #"high": barData[int(i)].high,
                              #"low": barData[int(i)].low,
                              "open": barData[int(i)].open,
                              "timestamp": barData[int(i)].timestamp})
            #i = i + interval
            i = i + 1

        #if self.timeInterval == TimeFrameUnit.Minute

        self.dataLock.release()

        print(self.data)


    #update stock's data when timer goes off
    def periodicDataUpdate(self):
        #if market isnt open, no point in periodic data updates
        if isMarketOpen(datetime.now(timezone.utc)):
            #do something with locks maybe, also currStock.stockUI.changeContents(currStock.data)
            if self.hasUpdatedLastMinute:
                self.initHistoricData()
            else:
                self.initHistoricData() #cant do this because it will overwrite websocket updates becasue of 15 minute delay


class singleStockUI(tk.Frame):
    def __init__(self, parent, data):
        tk.Frame.__init__(self, parent, bg='black')
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #get values to plot from data
        timeToPlot = [sub["timestamp"] for sub in data]
        valsToPlot = [sub["open"] for sub in data]

        self.fig = plt.figure()
        self.fig.tight_layout()
        self.fig.set_facecolor("none")

        self.stockPlot = self.fig.add_subplot(111)
        self.stockPlot.spines['top'].set_visible(False)
        self.stockPlot.spines['right'].set_visible(False)
        #self.stockPlot.spines['bottom'].set_visible(False)
        #self.stockPlot.spines['left'].set_visible(False)
        self.stockPlot.spines['bottom'].set_color('white')
        self.stockPlot.spines['left'].set_color('white')

        self.stockPlot.set_facecolor("none")
        #self.stockPlot.xaxis.label.set_color('white')
        self.stockPlot.tick_params(axis='x', colors='white')
        #self.stockPlot.yaxis.label.set_color('white')
        self.stockPlot.tick_params(axis='y', colors='white')


        #self.stockPlot.grid(axis='y', linestyle = "dashed", alpha = 0.30)
        self.stockPlot.margins(x=0)
        self.stockPlot.plot(timeToPlot, valsToPlot, color='red')

        canvas = FigureCanvasTkAgg(self.fig, self)
        canvas.draw()
        canvas.get_tk_widget().config(bg='black')

        self.priceLbl = tk.Label(self, text="Price:", font=('Helvetica', '20', "bold"), fg="white", bg="black", anchor=tk.W, padx=40)
        #now geometrically place them (pack or grid). 
        #ORDER IS IMPORTANT. Place smaller ones first to ensure they don't get covered by bigger ones.
        self.priceLbl.pack(side=tk.BOTTOM, fill = tk.BOTH, expand = 1, pady=(10,0))
        #self.priceLbl.grid(row=1, column=0, sticky="nsew")

        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        #canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        # toolbar = NavigationToolbar2Tk( canvas, self )
        # toolbar.update()
        # canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    #used to change contents of a stock on the stock view (like when changing the displayed stock)
    #data is a queue containing the data of the stock
    def changeContents(self, data):
        print("hi")
        timeToPlot = [sub["timestamp"] for sub in data]
        valsToPlot = [sub["open"] for sub in data]

        self.stockPlot.clear()

        #self.stockPlot.grid(axis='y', linestyle = "dashed", alpha = 0.30)
        self.stockPlot.margins(x=0)
        self.stockPlot.plot(timeToPlot, valsToPlot, color='red')

        self.fig.canvas.draw()





if __name__ == '__main__':
    now = datetime.now(timezone.utc)
    d = timedelta(days=31)
    requiredStart = now - d

    print(requiredStart)
