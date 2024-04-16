import tkinter as tk

import matplotlib
matplotlib.use('agg')
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from multiStockView import multiStockView
from stockObject import stockObject

from sys import platform

#called to update a stock figure when new data comes in
def animate(fig):
    print("hi")


# class singleStock(tk.Frame):
#     def __init__(self, parent):
#         tk.Frame.__init__(self, parent, bg='black')

#         self.fig = plt.figure()
#         self.stockPlot = self.fig.add_subplot(111)
#         self.stockPlot.plot([1,2], [2,3])

#         canvas = FigureCanvasTkAgg(self.fig, self)
#         canvas.draw()
#         canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

#         # toolbar = NavigationToolbar2Tk( canvas, self )
#         # toolbar.update()
#         # canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

#     #used to change contents of a stock on the stock view (like when changing the displayed stock)
#     def changeContents(self):
#         print("hi")

#         animate(self.fig)


# #supports different types of allStockViews, like top x movers, a view of x select stocks, top x stocks from your portfolio
# class allStockView(tk.Frame):
#     def __init__(self, parent, controller, dim):
#         tk.Frame.__init__(self, parent, bg='black')
#         # button = tk.Button(self, text="Visit trade view",
#         #                     command=lambda: controller.showPage("tradeView"))
#         # button.pack()

#         self.stocks = {}

#         for i in range(dim[0]):
#             for j in range(dim[1]):
#                 currStock = singleStock(self)
#                 currStock.grid(row=i, column=j, sticky="nsew", padx=(20, 20), pady=(20, 20))
#                 self.stocks[(i,j)] = currStock




#popup window to confirm a stock trade
class tradeConfirmation(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg='black')


#view when trading a stock
class tradeView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='red')
        button = tk.Button(self, text="Visit trade view",
                            command=lambda: controller.showPage("allStocks"))
        button.pack()


class view():
    #dim = tuple of what the allStockView grid dimensions will be
    def __init__(self, dim):
        self.tk = tk.Tk()
        self.tk.configure(bg='black')

        if platform == "linux": #If Linux (Raspberry Pi): 
            #self.tk.attributes('-zoomed', True)
            print("h")
        elif platform == "darwin" or platform == "win32": #If Windows or MacOS:
            self.tk.state('zoomed') 
        
        #self.tk.bind("<Return>", self.hi)

        self.mainFrame = tk.Frame(self.tk, bg='black')
        self.mainFrame.pack(side = tk.TOP, fill=tk.BOTH, expand = tk.YES)
        self.mainFrame.grid_rowconfigure(0, weight=1) #give grid rowIndex 0 full weight (take up full screen)
        self.mainFrame.grid_columnconfigure(0, weight=1) #give grid colIndex 0 full weight (take up full screen)


        self.allPages = {} #each page is a frame

        trade = tradeView(self.mainFrame, self)
        trade.grid(row=0, column=0, sticky="nsew")
        self.allPages["tradeView"] = trade


        #starting page
        self.showPage("tradeView")


    def showPage(self, page):
        frameToShow = self.allPages[page]
        frameToShow.tkraise()
        

if __name__ == '__main__':
    app = view((2,2))
    app.tk.mainloop() #is blocking
