from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import MarketMoversRequest
from alpaca.data.historical.screener import ScreenerClient
from alpaca.data.models.screener import Movers, Mover
from alpaca.data.live import StockDataStream
import yaml

from multiStockView import multiStockView
from stockObject import stockObject

#gainOrLoss = "gain" or default for top gainers, "loss" for top losers. currentStockList = multiStockView object
def getTopMovers(api_key, secret_key, currentStockList, gainOrLoss):
    client = ScreenerClient(api_key, secret_key)
    movers_request = MarketMoversRequest(top=10)

    market_movers = client.get_market_movers(movers_request) #returns a Movers class object
    print(market_movers.gainers[0].change) #access gainers field of Movers object, access Mover at list position 0, access change field of Mover object 

    if gainOrLoss == "loss":
        market_losers = market_movers.losers
        for i in range(currentStockList.size):
            currStock = stockObject(market_losers[i].symbol)
            currentStockList.replaceStock(i, currStock)
    else:
        market_gainers = market_movers.gainers
        for i in range(currentStockList.size):
            currStock = stockObject(market_gainers[i].symbol)
            currentStockList.replaceStock(i, currStock)

    return


