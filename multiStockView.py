from view import recalibrateView
from constantTimer import constantTimer
from collections import deque
import threading
from utilities import waitForMinuteToStart
from datetime import datetime, timedelta, timezone
import concurrent.futures
from alpaca.data.live import StockDataStream
import time

import voiceControl

class multiStockView:

    def __init__(self, api_key, secret_key, size, timerInterval):
        self.api_key = api_key
        self.secret_key = secret_key
        self.size = size #max number of stocks in view, determines grid layout (4 means 2x2)

        self.stocks = deque() #queue of stocks (for ordering purposes)
        self.stocksDict = {} #dictionary of stocks (for fast lookup purposes). key = symbol, value = stock

        #timer and timerHandle responsible for periodically updating all stock data points if needed
        self.timer = constantTimer(timerInterval, self.timerHandle)
        threading.Thread(target=self.setupTimer).start()

        #threadpool to handle updating stock data when needed (after timer goes off)
        self.updateExecutor = concurrent.futures.ThreadPoolExecutor(max_workers=self.size)

        #new thread for handling websocket connection for incoming live data for stocks
        threading.Thread(target=self.setupWebsocket).start()

        threading.Thread(target=voiceControl.main).start()


    #data will be in trade format
    async def websocketHandlerTrades(self, data):
        print(data)
        currStock = self.stocksDict[data.symbol]
        
        currStock.dataLock.acquire()
        currStock.data[-1] = 1

        currStock.dataLock.release()
        return


    def updateWebsocketConnections(self):
        self.websocket_client.subscribe_trades(self.websocketHandlerTrades, *self.stocksDict.keys())


    def setupWebsocket(self):
        self.websocket_client = StockDataStream(self.api_key, self.secret_key)
        self.websocket_client.subscribe_trades(self.websocketHandlerTrades, *self.stocksDict.keys())
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
        
        del self.stocks[i]
        del self.stocksDict[stockToRemoveSymbol]

        recalibrateView()


    #replaces a stock given its symbol
    def replaceStock(self, stockToReplaceSymbol, newStock):
        i = 0
        for currStock in self.stocks:
            if currStock.symbol == stockToReplaceSymbol:
                break
            i = i+1

        if i == len(self.stocks):
            print("stock to remove is not a current stock")
            return
        
        self.stocks[i] = newStock
        del self.stocksDict[stockToReplaceSymbol]
        self.stocksDict[newStock.symbol] = newStock
        
        recalibrateView()


    #adds a stock, newStock is a stockObject
    def addStock(self, newStock):
        if self.stocksDict.get(newStock.symbol) != None:
            print("stock to add is already present")
            return
        
        self.stocks.append(newStock)
        self.stocksDict[newStock.symbol] = newStock

        if len(self.stocks) > self.size:
            removed = self.stocks.popleft()
            del self.stocksDict[removed.symbol]

        recalibrateView()