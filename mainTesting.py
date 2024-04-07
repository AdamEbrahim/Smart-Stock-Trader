import alpacaAPI
from alpaca.data.live import StockDataStream
from alpaca.data.timeframe import TimeFrameUnit
import yaml
import threading
import asyncio
import time
import concurrent.futures

from multiStockView import multiStockView
from stockObject import stockObject

#todo: acquire and release lock of stock object when changing queue
async def trade_data_handler1(data):
    print("trade 1")
    print(data)
    return


#symbols = list of string symbols of stocks
def setupWebsocket(api_key, secret_key, symbols):
    print(api_key)

    global websocket_client1
    websocket_client1 = StockDataStream(api_key, secret_key)
    websocket_client1.subscribe_trades(trade_data_handler1, *symbols)
    websocket_client1.run()
    # print("hi")

def websocketSwitchHandler(stockList):
    while True:
        for stock in stockList:
            websocket_client1.subscribe_trades(trade_data_handler1, stock)
            time.sleep(5)


        


if __name__ == '__main__':

    #obtain API keys and secret keys from config file
    with open('config.yml', 'r') as file:
        keys = yaml.safe_load(file)

    stockList = ["AAPL", "SPY"]

    #executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    #executor.submit(setupWebsocket, keys['LIVE_API_KEY'], keys['LIVE_SECRET_KEY'], stockList)
    # time.sleep(5)
    # executor.submit(websocketSwitchHandler, stockList)
    #setupWebsocket(keys['LIVE_API_KEY'], keys['LIVE_SECRET_KEY'], stockList)


    # threading.Thread(target=setupWebsocket, args=(keys['LIVE_API_KEY'], keys['LIVE_SECRET_KEY'], stockList)).start()
    # time.sleep(3)
    # threading.Thread(target=websocketSwitchHandler, args=[stockList]).start()

    #while True:
        #print("hitwo")
        #time.sleep(.25)


    #setupWebsocket(keys['LIVE_API_KEY'], keys['LIVE_SECRET_KEY'], "SPY")

    # stockList = multiStockView(keys['LIVE_API_KEY'], keys['LIVE_SECRET_KEY'], 4, 60)
    # currStock = stockObject(keys['LIVE_API_KEY'], keys['LIVE_SECRET_KEY'], "AAPL", TimeFrameUnit.Week)
    # stockList.addStock(currStock)

    # alpacaAPI.getTopMovers(keys['LIVE_API_KEY'], keys['LIVE_SECRET_KEY'], stockList, "gain")
    # print(stockList.stocks)

    #alpacaAPI.historicalTesting(keys['LIVE_API_KEY'], keys['LIVE_SECRET_KEY'])

    #currStock = stockObject(keys['LIVE_API_KEY'], keys['LIVE_SECRET_KEY'], "AAPL", TimeFrameUnit.Day)

    alpacaAPI.executeTrade(keys['PAPER_API_KEY'], keys['PAPER_SECRET_KEY'], True, True)




