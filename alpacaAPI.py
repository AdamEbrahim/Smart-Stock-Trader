from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import MarketMoversRequest, StockLatestQuoteRequest, StockQuotesRequest, StockLatestTradeRequest, StockTradesRequest
from alpaca.data.historical.screener import ScreenerClient
from alpaca.data.models.screener import Movers, Mover
from alpaca.data.enums import DataFeed
from datetime import datetime

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

# im gonna get the bar data minute wise to do historical data
def historicalTesting(api_key, secret_key):
    client = StockHistoricalDataClient(api_key, secret_key)

    multiSymbolRequest1 = StockLatestTradeRequest(symbol_or_symbols="AAPL")
    multiSymbolRequest2 = StockTradesRequest(symbol_or_symbols="AAPL", start=datetime(2024, 4, 3, 19, 59, 55), end=datetime(2024, 4, 3, 20), limit=10, feed=DataFeed.IEX)

    latestTrades = client.get_stock_latest_trade(multiSymbolRequest1)
    regularTrades = client.get_stock_trades(multiSymbolRequest2)

    print("latest trades:")
    print(latestTrades)
    print("regular trades:")
    print(regularTrades)


