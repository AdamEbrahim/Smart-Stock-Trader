from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import MarketMoversRequest
from alpaca.data.historical.screener import ScreenerClient
from alpaca.data.models.screener import Movers, Mover
from alpaca.data.live import StockDataStream
import yaml

def getTopMovers(api_key, secret_key):
    client = ScreenerClient(api_key, secret_key)
    movers_request = MarketMoversRequest(top=10)

    market_movers = client.get_market_movers(movers_request) #returns a Movers class object
    print(market_movers.gainers[0].change) #access gainers field of Movers object, access Mover at list position 0, access change field of Mover object  


