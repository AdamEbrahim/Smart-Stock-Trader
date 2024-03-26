import alpacaAPI
import yaml

async def quote_data_handler(data):
    print(data)

if __name__ == '__main__':

    #obtain API keys and secret keys from config file
    with open('config.yml', 'r') as file:
        keys = yaml.safe_load(file)

    alpacaAPI.getTopMovers(keys['LIVE_API_KEY'], keys['LIVE_SECRET_KEY'])

    # client = StockHistoricalDataClient(keys['LIVE_API_KEY'], keys['LIVE_SECRET_KEY'])

    # # multi symbol request - single symbol is similar
    # multisymbol_request_params = StockLatestQuoteRequest(symbol_or_symbols=["SPY", "GLD", "TLT"])

    # latest_multisymbol_quotes = client.get_stock_latest_quote(multisymbol_request_params)

    # gld_latest_ask_price = latest_multisymbol_quotes["GLD"].ask_price
    # print(gld_latest_ask_price)

    # websocket_client = StockDataStream(keys['LIVE_API_KEY'], keys['LIVE_SECRET_KEY'])
    # websocket_client.subscribe_quotes(quote_data_handler, "SPY")
    # websocket_client.run()

