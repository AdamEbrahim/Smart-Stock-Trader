from view import recalibrateView
from constantTimer import constantTimer
from collections import deque
import threading
from utilities import waitForMinuteToStart
from datetime import datetime, timedelta, timezone
import concurrent.futures
from alpaca.data.live import StockDataStream

class multiStockView:

    def __init__(self, api_key, secret_key, size, timerInterval):
        self.size = size #max number of stocks in view, determines grid layout (4 means 2x2)

        self.stocks = deque()
        self.stockSymbols = deque()

        #timer and timerHandle responsible for periodically updating all stock data points if needed
        self.timer = constantTimer(timerInterval, self.timerHandle)
        threading.Thread(target=self.setupTimer).start()

        #threadpool to handle updating stock data when needed (after timer goes off)
        self.updateExecutor = concurrent.futures.ThreadPoolExecutor(max_workers=self.size)

        #handle websocket connection for incoming live data for stocks
        self.websocket_client = StockDataStream(api_key, secret_key)
        self.websocket_client.subscribe_trades(self.websocketHandler, *self.stockSymbols)
        self.websocket_client.run()

    
    async def websocketHandler(self, data):
        print(data)
        return


    def updateWebsocketConnections(self):
        self.websocket_client.subscribe_trades(self.websocketHandler, *self.stockSymbols)


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
        del self.stockSymbols[i]

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
        self.stockSymbols[i] = newStock.symbol
        
        recalibrateView()


    #adds a stock, newStock is a stockObject
    def addStock(self, newStock):
        self.stocks.append(newStock)
        self.stockSymbols.append(newStock.symbol)

        if len(self.stocks) > self.size:
            self.stocks.popleft()
            self.stockSymbols.popleft()

        recalibrateView()