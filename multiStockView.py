from view import recalibrateView
from constantTimer import constantTimer
from collections import deque

class multiStockView:

    def __init__(self, size, timerInterval):
        self.size = size #max number of stocks in view, determines grid layout (4 means 2x2)

        self.stocks = deque()

        #timer and timerHandle responsible for periodically updating all stock data points if needed
        self.timer = constantTimer(timerInterval, self.timerHandle)
        self.timer.start()


    def timerHandle(self):
        for i in range(len(self.stocks)):
            currStock = self.stocks[i]
        

    #removes a stock given its symbol
    def removeStock(self, stockToRemoveSymbol):
        currIndex = -1
        for i in range(len(self.stocks)):
            if self.stocks[i].symbol == stockToRemoveSymbol:
                currIndex = i
                break

        if currIndex == -1:
            print("stock to remove is not a current stock")
            return
        
        del self.stocks[currIndex]

        recalibrateView()


    #replaces a stock given its symbol
    def replaceStock(self, stockToReplaceSymbol, newStock):
        currIndex = -1
        for i in range(len(self.stocks)):
            if self.stocks[i].symbol == stockToReplaceSymbol:
                currIndex = i
                break

        if currIndex == -1:
            print("stock to replace is not a current stock")
            return
        
        self.stocks[currIndex] = newStock
        
        recalibrateView()


    #adds a stock, newStock is a stockObject
    def addStock(self, newStock):
        self.stocks.append(newStock)

        if len(self.stocks) > self.size:
            self.stocks.popleft()

        recalibrateView()