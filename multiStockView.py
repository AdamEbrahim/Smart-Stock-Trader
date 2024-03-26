from view import recalibrateView

class multiStockView:

    def __init__(self, size):
        self.size = size #number of stocks in view

        self.numStocks = 0
        self.stocks = [None for i in range(size)]
        

    #removes the stock at index currIndex
    def removeStock(self, currIndex):
        if currIndex >= self.numStocks or currIndex < 0:
            return
        
        for i in range(currIndex, self.numStocks):
            if i == self.numStocks - 1:
                self.stocks[i] = None
            else:
                self.stocks[i] = self.stocks[i+1]

        self.numStocks = self.numStocks - 1

        recalibrateView()


    #replaces a stock at index currIndex
    def replaceStock(self, currIndex, newStock):
        if currIndex >= self.size or currIndex < 0:
            return
        
        if currIndex >= self.numStocks:
            self.stocks[self.numStocks] = newStock
            self.numStocks = self.numStocks + 1
        else:
            self.stocks[currIndex] = newStock
        
        recalibrateView()


    #adds a stock
    def addStock(self, newStock):
        if self.numStocks < self.size:
            self.stocks[self.numStocks] = newStock
            self.numStocks = self.numStocks + 1
        else:
            for i in range(0, self.size):
                if i == self.size - 1:
                    self.stocks[i] = newStock
                else:
                    self.stocks[i] = self.stocks[i+1]

        recalibrateView()