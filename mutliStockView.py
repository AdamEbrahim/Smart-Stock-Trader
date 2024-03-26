from view import recalibrateView

class multiStockView:

    def __init__(self, size):
        self.size = size #number of stocks in view
        self.stocks = [None for i in range(size)]
        


    def removeStock(self, i):
        recalibrateView()

    def replaceStock(self, i, newStock):
        recalibrateView()

    def addStock(self, newStock):
        recalibrateView()