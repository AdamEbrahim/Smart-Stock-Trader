import alpacaAPI
from alpaca.data.live import StockDataStream
from alpaca.data.timeframe import TimeFrameUnit
from alpaca.trading.enums import OrderSide, TimeInForce
import yaml
import threading
import asyncio
import time
import concurrent.futures

from multiStockView import multiStockView
from stockObject import stockObject
from stockTrader import stockTrader


if __name__ == '__main__':

    #obtain API keys and secret keys from config file
    with open('config.yml', 'r') as file:
        keys = yaml.safe_load(file)

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

    # alpacaAPI.executeTradeMarketQty(keys['PAPER_API_KEY'], keys['PAPER_SECRET_KEY'], True, "AAPL", OrderSide.SELL, 3.2)
    # alpacaAPI.executeTradeMarketValue(keys['PAPER_API_KEY'], keys['PAPER_SECRET_KEY'], True, "AAPL", OrderSide.BUY, 145.35)
    # alpacaAPI.executeTradeLimitQty(keys['PAPER_API_KEY'], keys['PAPER_SECRET_KEY'], True, "AAPL", OrderSide.BUY, 2.75, 140.3)
    # alpacaAPI.executeTradeLimitValue(keys['PAPER_API_KEY'], keys['PAPER_SECRET_KEY'], True, "AAPL", OrderSide.BUY, 185.6, 140.75)

    trader = stockTrader(keys['PAPER_API_KEY'], keys['PAPER_SECRET_KEY'], True, (2,2), keys['MONITOR_RESOLUTION'], keys['GUI_SETUP_TIME'], keys['PIR_PIN'], keys['LED_PIN'], keys['MONITOR_TIMEOUT'])

    #--CANNOT LET MAIN THREAD DIE OR ELSE THERE ARE ERRORS WITH SUBMITTING THREADPOOL TASKS--#
    #currStock2 = stockObject(keys['LIVE_API_KEY'], keys['LIVE_SECRET_KEY'], "GOOG", TimeFrameUnit.Week)
    while True:
        time.sleep(5)
        #stockList.addStock(currStock2)

