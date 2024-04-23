from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import MarketMoversRequest, StockLatestQuoteRequest, StockQuotesRequest, StockLatestTradeRequest, StockTradesRequest, StockBarsRequest, StockLatestBarRequest
from alpaca.data.historical.screener import ScreenerClient
from alpaca.data.models.screener import Movers, Mover
from alpaca.data.enums import DataFeed
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from datetime import datetime, timezone

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest, GetAssetsRequest
from alpaca.trading.enums import OrderSide, TimeInForce, AssetClass
from alpaca.trading.models import TradeAccount

from alpaca.common.exceptions import APIError

from multiStockView import multiStockView
from stockObject import stockObject

from utilities import getLastClose, isMarketOpen

#gainOrLoss = "gain" or default for top gainers, "loss" for top losers. currentStockList = multiStockView object
def getTopMovers(api_key, secret_key, currentStockList, gainOrLoss):
    client = ScreenerClient(api_key, secret_key)
    movers_request = MarketMoversRequest(top=10)

    market_movers = client.get_market_movers(movers_request) #returns a Movers class object
    print(market_movers.gainers[0].change) #access gainers field of Movers object, access Mover at list position 0, access change field of Mover object 

    if gainOrLoss == "loss":
        market_losers = market_movers.losers
        for i in range(currentStockList.size):
            currStock = stockObject(api_key, secret_key, market_losers[i].symbol, TimeFrameUnit.Day, currentStockList) #default timeframe of day
            currentStockList.addStock(currStock)
    else:
        market_gainers = market_movers.gainers
        for i in range(currentStockList.size):
            currStock = stockObject(api_key, secret_key, market_gainers[i].symbol, TimeFrameUnit.Day, currentStockList) #default timeframe of day
            currentStockList.addStock(currStock)

    return

def requestPortfolio(api_key, secret_key):
    client = TradingClient(api_key, secret_key)
    return client.get_all_positions()

def getPortfolio(api_key, secret_key, currentStockList):
    positions = requestPortfolio(api_key, secret_key)

    #remove currently displayed stocks
    toRemove = list(currentStockList.stocksDict.keys())

    for i in range(len(toRemove)):
        currentStockList.removeStock(toRemove[i])

    for i in range(len(positions)): #if own more stocks that max view size will only show the last 4 because of how addStocks works
        currStock = stockObject(api_key, secret_key, positions[i].symbol, TimeFrameUnit.Day, currentStockList) #default timeframe of day
        currentStockList.addStock(currStock)

# im gonna get the bar data minute wise to do historical data
def historicalTesting(api_key, secret_key):
    client = StockHistoricalDataClient(api_key, secret_key)

    #Trades
    # multiSymbolRequest1 = StockLatestTradeRequest(symbol_or_symbols="AAPL")
    # multiSymbolRequest2 = StockTradesRequest(symbol_or_symbols="AAPL", start=datetime(2024, 4, 3, 19, 59, 55), end=datetime(2024, 4, 3, 20), limit=10, feed=DataFeed.IEX)

    # latestTrades = client.get_stock_latest_trade(multiSymbolRequest1)
    # regularTrades = client.get_stock_trades(multiSymbolRequest2)

    #Bars
    # multiSymbolRequestBars1 = StockLatestBarRequest(symbol_or_symbols=["AAPL", "SPY"])
    multiSymbolRequestBars2 = StockBarsRequest(symbol_or_symbols="AAPL", timeframe=TimeFrame(1, TimeFrameUnit.Day), start=datetime(2024, 4, 3))
    multiSymbolRequestBars3 = StockBarsRequest(symbol_or_symbols="AAPL", timeframe=TimeFrame(1, TimeFrameUnit.Hour), start=datetime(2024, 4, 3))

    # latestBars = client.get_stock_latest_bar(multiSymbolRequestBars1)
    regularBars = client.get_stock_bars(multiSymbolRequestBars2)
    regularBars2 = client.get_stock_bars(multiSymbolRequestBars3)

    print("regular bars 1:")
    print(regularBars)
    print("regular bars 2:")
    print(regularBars2)

#used to determine if you have enough of a stock to sell since no shorting. return -1 if false, 0 if true
def enoughToSellQty(trading_client, stockSymbol, quantity):
    
    positions = trading_client.get_all_positions()
    print(positions)

    found = False
    for position in positions:
        if position.symbol == stockSymbol:
            if float(position.qty_available) < float(quantity): #not sure if need to use qty_available or qty
                print("not enough of stock to sell the given quantity with no shorting")
                return -1
            
            found = True
            break

    if not found:
        print("stock to sell not found, cannot execute sale without shorting")
        return -1
    
    return 0

#used to determine if you have enough of a stock to sell since no shorting. return -1 if false, 0 if true
def enoughToSellVal(trading_client, stockSymbol, dollarValue):
    
    positions = trading_client.get_all_positions()
    print(positions)

    found = False
    for position in positions:
        if position.symbol == stockSymbol:
            if float(position.market_value) < float(dollarValue):
                print("not enough of stock to sell the given quantity with no shorting")
                return -1
            
            found = True
            break

    if not found:
        print("stock to sell not found, cannot execute sale without shorting")
        return -1
    
    return 0

#execute a market trade (buy or sell) based on a quantity of stocks to buy or sell
#isPaper = true if want paper trades, orderSide is an OrderSide enum for buy or sell (OrderSide.BUY or OrderSide.SELL)
#if paper, make sure passed in api_key and secret_key are for paper, otherwise make sure they are for live
def executeTradeMarketQty(api_key, secret_key, isPaper, stockSymbol, orderSide, quantity):
    trading_client = TradingClient(api_key, secret_key, paper=isPaper)
    
    #used to determine if you have enough of a stock to sell since no shorting
    if orderSide == OrderSide.SELL:
        if enoughToSellQty(trading_client, stockSymbol, quantity) == -1:
            return

    order_data = MarketOrderRequest(
                    symbol=stockSymbol,
                    qty=quantity,
                    side=orderSide,
                    time_in_force=TimeInForce.DAY
                    )
    
    #below checks to make sure you have sufficient buying power for buys, and makes sure nothing goes wrong for sells
    order = 0
    try: #format of api_error is "raise APIError(error, http_error)"
        order = trading_client.submit_order(order_data)
    except APIError as err:
        x = err.args
        print("there was an error: ")
        print(x)


#execute a market trade (buy or sell) based on the dollar value of stocks to buy or sell
#isPaper = true if want paper trades, orderSide is an OrderSide enum for buy or sell (OrderSide.BUY or OrderSide.SELL)
#if paper, make sure passed in api_key and secret_key are for paper, otherwise make sure they are for live
def executeTradeMarketValue(api_key, secret_key, isPaper, stockSymbol, orderSide, dollarValue):
    trading_client = TradingClient(api_key, secret_key, paper=isPaper)

    #used to determine if you have enough of a stock to sell since no shorting
    if orderSide == OrderSide.SELL:
        if enoughToSellVal(trading_client, stockSymbol, dollarValue) == -1:
            return

    order_data = MarketOrderRequest(
                    symbol=stockSymbol,
                    notional=dollarValue,
                    side=orderSide,
                    time_in_force=TimeInForce.DAY
                    )
        
    order = 0
    try: #format of api_error is "raise APIError(error, http_error)"
        order = trading_client.submit_order(order_data)
    except APIError as err:
        x = err.args
        print("there was an error: ")
        print(x)


#execute a limit trade (buy or sell) based on a quantity of stocks to buy or sell
#isPaper = true if want paper trades, orderSide is an OrderSide enum for buy or sell (OrderSide.BUY or OrderSide.SELL)
#limit = limit price
#if paper, make sure passed in api_key and secret_key are for paper, otherwise make sure they are for live
def executeTradeLimitQty(api_key, secret_key, isPaper, stockSymbol, orderSide, quantity, limit):
    trading_client = TradingClient(api_key, secret_key, paper=isPaper)

    #used to determine if you have enough of a stock to sell since no shorting
    if orderSide == OrderSide.SELL:
        if enoughToSellQty(trading_client, stockSymbol, quantity) == -1:
            return

    order_data = LimitOrderRequest(
                    symbol=stockSymbol,
                    limit_price=limit,
                    qty=quantity,
                    side=orderSide,
                    time_in_force=TimeInForce.DAY
                    )
        
    order = 0
    try: #format of api_error is "raise APIError(error, http_error)"
        order = trading_client.submit_order(order_data)
    except APIError as err:
        x = err.args
        print("there was an error: ")
        print(x)


#execute a limit trade (buy or sell) based on the dollar value of stocks to buy or sell
#isPaper = true if want paper trades, orderSide is an OrderSide enum for buy or sell (OrderSide.BUY or OrderSide.SELL)
#limit = limit price
#if paper, make sure passed in api_key and secret_key are for paper, otherwise make sure they are for live
def executeTradeLimitValue(api_key, secret_key, isPaper, stockSymbol, orderSide, dollarValue, limit):
    trading_client = TradingClient(api_key, secret_key, paper=isPaper)

    #used to determine if you have enough of a stock to sell since no shorting
    if orderSide == OrderSide.SELL:
        if enoughToSellVal(trading_client, stockSymbol, dollarValue) == -1:
            return

    order_data = LimitOrderRequest(
                    symbol=stockSymbol,
                    limit_price=limit,
                    notional=dollarValue,
                    side=orderSide,
                    time_in_force=TimeInForce.DAY
                    )
        
    order = 0
    try: #format of api_error is "raise APIError(error, http_error)"
        order = trading_client.submit_order(order_data)
    except APIError as err:
        x = err.args
        print("there was an error: ")
        print(x)


def getAccountDetails(api_key, secret_key, isPaper):
    trading_client = TradingClient(api_key, secret_key, paper=isPaper)

    account = trading_client.get_account()


def getAssets(api_key, secret_key, isPaper):
    trading_client = TradingClient(api_key, secret_key, paper=isPaper)

    search_params = GetAssetsRequest(asset_class=AssetClass.CRYPTO)

    assets = trading_client.get_all_assets(search_params)

#return true if profit on the day, false if loss on the day (or last day markets open)
def dailyProfitOrLoss(api_key, secret_key):
    positions = requestPortfolio(api_key, secret_key)

    client = StockHistoricalDataClient(api_key, secret_key)
    now = datetime.now(timezone.utc)
    marketUp = isMarketOpen(now)

    if not marketUp:
        now = getLastClose(now)

    requiredStart = now.date()

    total = 0
    for i in range(len(positions)):
        symbol = positions[i].symbol
        numOwned = positions[i].qty
        barsRequest = StockBarsRequest(symbol_or_symbols=symbol, timeframe=TimeFrame.Day, start=requiredStart)
        bars = client.get_stock_bars(barsRequest)
        barData = bars[symbol]
        openPrice = barData[0].open

        latestTradeRequest = StockLatestTradeRequest(symbol_or_symbols=symbol)
        trade = client.get_stock_latest_trade(latestTradeRequest)
        currPrice = trade[symbol].price

        total = total + ((currPrice - openPrice) * float(numOwned))

    print(total)
    if total >= 0:
        return True
    else:
        return False


