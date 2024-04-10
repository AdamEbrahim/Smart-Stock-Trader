import tkinter as tk


class singleStock(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg='black')


#supports different types of allStockViews, like top x movers, a view of x select stocks, top x stocks from your portfolio
class allStockView(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg='black')


#view when trading a stock
class tradeView(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg='black')


class view():
    def __init__(self):
        self.tk = tk.Tk()
        self.tk.configure(bg='black')
        self.tk.state('zoomed')
        self.tk.bind("<Return>", self.hi)

        self.mainFrame = tk.Frame(self.tk, bg='black')
        self.mainFrame.pack(side = tk.TOP, fill=tk.BOTH, expand = tk.YES)
        self.bottomFrameTesting = tk.Frame(self.tk, bg='white')
        self.bottomFrameTesting.pack(side = tk.BOTTOM, fill=tk.BOTH, expand = tk.YES)

        self.allStocks = allStockView(self.mainFrame)
        self.allStocks.pack(side = tk.RIGHT, fill=tk.BOTH, expand=tk.YES)

    def hi(self, event=None):
        print('hi')
        return
        

if __name__ == '__main__':
    app = view()
    app.tk.mainloop() #is blocking


def recalibrateView():
    print("recalibrating view")