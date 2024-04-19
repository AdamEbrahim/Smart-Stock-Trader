from constantTimer import constantTimer
from collections import deque
import threading
from utilities import waitForMinuteToStart
from datetime import datetime, timedelta, timezone
import concurrent.futures
from alpaca.data.live import StockDataStream
import time

import voiceControl

#UI stuff
import tkinter as tk
from stockObject import singleStockUI

class multiStockView:
    #dim = tuple (x,y)
    def __init__(self, api_key, secret_key, timerInterval, parentUI, dim):
        self.api_key = api_key
        self.secret_key = secret_key
        self.dim = dim
        self.size = dim[0] * dim[1] #max number of stocks in view

        self.stocks = deque() #queue of stocks (for ordering purposes)
        self.stocksDict = {} #dictionary of stocks (for fast lookup purposes). key = symbol, value = stock

        #timer and timerHandle responsible for periodically updating all stock data points if needed
        self.timer = constantTimer(timerInterval, self.timerHandle)
        threading.Thread(target=self.setupTimer).start()

        #threadpool to handle updating stock data when needed (after timer goes off)
        self.updateExecutor = concurrent.futures.ThreadPoolExecutor(max_workers=self.size)

        #new thread for handling websocket connection for incoming live data for stocks
        threading.Thread(target=self.setupWebsocket).start()

        #threading.Thread(target=voiceControl.main).start()

        #UI object (allStockView Frame)
        self.multiStockUI = self.initUI(parentUI, dim)


    # def updateWebsocketConnections(self):
    #     print(list(self.stocksDict.keys()))
    #     self.websocket_client.subscribe_trades(self.websocketHandlerTrades, *list(self.stocksDict.keys()))


    def setupWebsocket(self):
        self.websocket_client = StockDataStream(self.api_key, self.secret_key)
        self.websocket_client.subscribe_trades(self.websocketHandlerTrades, *list(self.stocksDict.keys()))
        self.websocket_client.run()


    def timerHandle(self):
        print(datetime.now())

        for currStock in self.stocks:
            #use the threadpoolexecutor to handle updating stuff for the different stocks so we don't lose our timer's precision
            self.updateExecutor.submit(currStock.periodicDataUpdate)


    def setupTimer(self):
        waitForMinuteToStart()
        self.timerHandle() #make sure to call the timer handle first because we have hit that minute mark
        self.timer.start() #start the repeating timer, destroys thread that called setupTimer


    #This function is necessary becasue we have to separately destroy single stock widgets (they don't go away when we delete stock object)
    #MUST CALL BEFORE DESTROYING STOCKOBJECT
    #stockObj is an actual stockObject whose stockUI widget we want to destroy
    def removeStockWidget(self, stockObj):
        stockObj.stockUI.destroy()
        del stockObj.stockUI


    #removes a stock given its symbol
    def removeStock(self, stockToRemoveSymbol):
        i = 0
        for currStock in self.stocks:
            if currStock.symbol == stockToRemoveSymbol:
                break
            i = i+1

        if i == len(self.stocks):
            print("stock to remove is not a current stock")
            return
        
        self.websocket_client.unsubscribe_trades(stockToRemoveSymbol)
        del self.stocksDict[stockToRemoveSymbol]
        self.removeStockWidget(self.stocks[i]) #must remove stock widget before destroying stockObject
        del self.stocks[i]

        self.multiStockUI.recalibrateView(self.dim, self.stocks)


    #replaces a stock given its symbol
    def replaceStock(self, stockToReplaceSymbol, newStock):
        if self.stocksDict.get(newStock.symbol) != None:
            print("Stock you are trying to replace another stock with is already present. Please remove it first.")
            return
        
        i = 0
        for currStock in self.stocks:
            if currStock.symbol == stockToReplaceSymbol:
                break
            i = i+1

        if i == len(self.stocks):
            print("stock to replace is not a current stock")
            return
        
        temp = self.stocks[i]
        self.removeStockWidget(temp) #must remove stock widget before destroying stockObject

        self.stocks[i] = newStock

        self.websocket_client.unsubscribe_trades(stockToReplaceSymbol)
        del temp
        del self.stocksDict[stockToReplaceSymbol]

        self.stocksDict[newStock.symbol] = newStock
        
        self.multiStockUI.recalibrateView(self.dim, self.stocks)


    #adds a stock, newStock is a stockObject
    def addStock(self, newStock):
        if self.stocksDict.get(newStock.symbol) != None:
            print("stock to add is already present")
            return
        
        self.stocks.append(newStock)
        self.stocksDict[newStock.symbol] = newStock
        self.websocket_client.subscribe_trades(self.websocketHandlerTrades, newStock.symbol)

        if len(self.stocks) > self.size:
            removed = self.stocks.popleft()
            symb = removed.symbol

            self.removeStockWidget(removed) #must remove stock widget before destroying stockObject
            self.websocket_client.unsubscribe_trades(symb)
            del removed
            del self.stocksDict[symb]

        self.multiStockUI.recalibrateView(self.dim, self.stocks)

    #data will be in trade format
    async def websocketHandlerTrades(self, data):
        print(data)

        currStock = self.stocksDict.get(data.symbol)
        if currStock == None: #hasn't unsubsribed from a stock that should be removed yet
            print("received websocket data from stock that should have been removed")
            return
        
        currStock.dataLock.acquire()
        currStock.data[-1]["open"] = data.price
        currStock.data[-1]["timestamp"] = data.timestamp
        print(currStock.symbol)

        currStock.dataLock.release()

        #show updated data in stock UI plot
        currStock.stockUI.changeContents(currStock.data)

        return
    
    #returns the allStockView UI object
    def initUI(self, parentUI, dim):
        ui = allStockView(parentUI.mainFrame, parentUI, dim)
        ui.grid(row=0, column=0, sticky="nsew")
        parentUI.allPages["allStocks"] = ui

        return ui


    

#supports different types of allStockViews, like top x movers, a view of x select stocks, top x stocks from your portfolio
class allStockView(tk.Frame):
    def __init__(self, parent, controller, dim):
        tk.Frame.__init__(self, parent, bg='black')
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        # button = tk.Button(self, text="Visit trade view",
        #                     command=lambda: controller.showPage("tradeView"))
        # button.pack()

    #stocks is the stocks deque of the multiStockView parent object, where each stock contain singleStockUI Frames
    def recalibrateView(self, dim, stocks):

        for i in range(dim[0]):
            for j in range(dim[1]):

                index = i*dim[1] + j
                if index >= len(stocks):
                    return

                currStockUI = stocks[index].stockUI
                currStockUI.grid(row=i, column=j, sticky="nsew", padx=(20, 20), pady=(20, 20))