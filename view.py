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
from alpaca.trading.enums import OrderSide

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



#view when trading a stock
class tradeView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='red')
        button = tk.Button(self, text="Visit trade view",
                            command=lambda: controller.showPage("allStocks"))
        button.pack()

#popup window to confirm a stock trade
class tradeConfirmation(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg='black')
        self.lblPre = tk.Label(self, text="Are you sure?", font=('Helvetica', '20', "bold"), fg="white", bg="black")
        self.lblMain = tk.Label(self, text="Empty", font=('Helvetica', '20', "bold"), fg="white", bg="black")
        self.lblPre.pack(side=tk.TOP, fill = tk.BOTH, expand = 1)
        self.lblMain.pack(side=tk.TOP, fill = tk.BOTH, expand = 1)

    def changeConfirmationText(self, tradeData):
        newTxt = ""
        if tradeData["purchaseOrSale"] == OrderSide.BUY:
            newTxt = newTxt + "Buy "
        elif tradeData["purchaseOrSale"] == OrderSide.SELL:
            newTxt = newTxt + "Sell "

        if "quantity" in tradeData["qtyOrVal"]:
            newTxt = newTxt + str(tradeData["number"]) + " shares of "
        elif "value" in tradeData["qtyOrVal"]:
            newTxt = newTxt + "$" + str(tradeData["number"]) + " worth of "

        newTxt = newTxt + tradeData["stockName"]

        if tradeData["marketOrLimit"] == "market":
            newTxt = newTxt + "."
        elif tradeData["marketOrLimit"] == "limit":
            newTxt = newTxt + " at limit price $" + str(tradeData["limitNumber"] + ".")

        self.lblMain.config(text=newTxt)

class view():
    #dim = tuple of what the allStockView grid dimensions will be, res = resolution (only linux), gui_setup_time (only raspberry pi)
    def __init__(self, dim, res, gui_setup_time):
        self.tk = tk.Tk()
        self.tk.configure(bg='black')

        self.res = res #doesnt matter except for linux
        self.state = True

        if platform == "linux": #If Linux (Raspberry Pi): 
            #self.tk.attributes('-zoomed', True)
            #self.tk.geometry('800x480+100+100')

            #ISSUE: RASPBERRY PI LINUX IS BUGGY AND FULLSCREEN ONLY WORKS SOMETIMES ON INITIALIZATION
            #THIS ENSURES AFTER SOME SETUP TIME (SECONDS * 1000 = MILLISECONDS) FULLSCREEN GETS TURNED ON 
            self.tk.after(gui_setup_time * 1000, lambda: self.tk.wm_attributes('-fullscreen', 'true'))

            self.tk.attributes('-fullscreen', True)
            #self.tk.geometry('800x480')
            self.tk.bind('<Return>', lambda e: self.toggleWin(e)) #bind return key with toggling fullscreen window, only on linux right now
            print("h")
        elif platform == "darwin" or platform == "win32": #If Windows or MacOS:
            self.tk.state('zoomed') 
        
        #self.tk.bind("<Return>", self.hi)

        self.mainFrame = tk.Frame(self.tk, bg='black')
        self.mainFrame.pack(side = tk.TOP, fill=tk.BOTH, expand = tk.YES)
        self.mainFrame.grid_rowconfigure(0, weight=1) #give grid rowIndex 0 full weight (take up full screen)
        self.mainFrame.grid_columnconfigure(0, weight=1) #give grid colIndex 0 full weight (take up full screen)

        # Bind the ESC key with the callback function to destroy window (entire tkinter gui)
        #buggy on macOS, should work fine on linux/windows
        self.tk.bind('<Escape>', lambda e: self.closeWin(e))


        self.allPages = {} #each page is a frame

        trade = tradeView(self.mainFrame, self)
        trade.grid(row=0, column=0, sticky="nsew")
        self.allPages["tradeView"] = trade

        tradeConf = tradeConfirmation(self.mainFrame, bg='black')
        tradeConf.grid(row=0, column=0, sticky="nsew")
        self.allPages["tradeConfirmation"] = tradeConf

        blackScreen = tk.Frame(self.mainFrame, bg='black')
        blackScreen.grid(row=0, column=0, sticky="nsew")
        self.allPages["blackScreen"] = blackScreen

        #starting page
        self.showPage("tradeView")


    def showPage(self, page):
        frameToShow = self.allPages[page]
        frameToShow.tkraise()

    def closeWin(self, event=None):
        self.tk.destroy() #buggy on macOS, should work fine on linux/windows

    #toggle window fullscreen on return key, only for linux because of fullscreen issues not allowing you to see toolbar
    def toggleWin(self, event=None):
        self.state = not self.state
        self.tk.attributes('-fullscreen', self.state)
        print(self.res) #very buggy on raspberry pi; further testing needed
        self.tk.geometry('200x200') #very buggy on rasbperry pi; further testing needed

        

if __name__ == '__main__':
    app = view((2,2))
    app.tk.mainloop() #is blocking
