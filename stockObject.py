from enum import Enum
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import MarketMoversRequest, StockLatestQuoteRequest, StockQuotesRequest, StockLatestTradeRequest, StockTradesRequest, StockBarsRequest, StockLatestBarRequest
import threading
from collections import deque
from datetime import datetime, timedelta, timezone
from utilities import isMarketOpen, isMarketOpenDay

#UI stuff
import tkinter as tk

import matplotlib
matplotlib.use('agg')
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

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

        #stock tkinter UI object
        self.stockUI = singleStockUI(parentUI)

        self.initHistoricData()


    #timeframeUnit is an enum alpaca.data.timeframe.TimeFrameUnit
    def changeTimeInterval(self, timeframeUnit):
        self.timeInterval = timeframeUnit
        print("changed time interval")
        self.initHistoricData()


    def initHistoricData(self):
        client = StockHistoricalDataClient(self.api_key, self.secret_key)
        requiredTimeFrame = 0
        requiredStart = 0
        now = datetime.now(timezone.utc)

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
                              "high": barData[int(i)].high,
                              "low": barData[int(i)].low,
                              "open": barData[int(i)].open,
                              "timestamp": barData[int(i)].timestamp})
            #i = i + interval
            i = i + 1

        #if self.timeInterval == TimeFrameUnit.Minute

        self.dataLock.release()

        print(self.data)


    #update stock's data when timer goes off
    def periodicDataUpdate(self):
        #do something with locks maybe?
        if self.hasUpdatedLastMinute:
            self.initHistoricData()
        else:
            self.initHistoricData()


class singleStockUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg='black')

        self.fig = plt.figure()
        self.stockPlot = self.fig.add_subplot(111)
        self.stockPlot.plot([1,2], [2,3])

        canvas = FigureCanvasTkAgg(self.fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # toolbar = NavigationToolbar2Tk( canvas, self )
        # toolbar.update()
        # canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    #used to change contents of a stock on the stock view (like when changing the displayed stock)
    def changeContents(self):
        print("hi")



if __name__ == '__main__':
    now = datetime.now(timezone.utc)
    d = timedelta(days=31)
    requiredStart = now - d

    print(requiredStart)
