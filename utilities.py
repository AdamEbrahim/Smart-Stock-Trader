import pandas_market_calendars as mcal
from datetime import datetime, timedelta, timezone
import pandas
import time

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.common.exceptions import APIError


#Check if market open at a specific dtObject time/date.
#return true or false
#dtObject is a datetime object, such as datetime.now(timezone.utc)
def isMarketOpen(dtObject):

    start = dtObject.isoformat(' ').split(' ')[0] #get the date
    iex = mcal.get_calendar("IEX")
    sched = iex.schedule(start_date=start, end_date=start)

    arr = sched.axes[0]

    if len(arr) < 1:
        print("false2")
        return False
    
    if arr[0].date().isoformat() != start:
        print("false")
        return False
    
    arr2 = sched.axes[1]

    dayOpen = sched.at[arr[0], arr2[0]].timestamp()
    dayClose = sched.at[arr[0], arr2[1]].timestamp()
    dtTimestamp = dtObject.timestamp()

    if dtTimestamp <= dayOpen or dtTimestamp >= dayClose:
        print("stocks closed at the current time")
        return False
    
    print("stocks open at the current time")
    return True
    


#Check if market open on the day of the passed in dtObject. 
#return true or false
#dtObject is a datetime object, such as datetime.now(timezone.utc)
def isMarketOpenDay(dtObject):
    start = dtObject.isoformat(' ').split(' ')[0] #get the date
    iex = mcal.get_calendar("IEX")
    sched = iex.schedule(start_date=start, end_date=start)

    arr = sched.axes[0]
    if len(arr) < 1:
        print("false2")
        return False
    
    if arr[0].date().isoformat() != start:  
        print("false")
        return False
    
    print("true")
    return True

def waitForMinuteToStart():
    now = datetime.now(timezone.utc)
    d1 = timedelta(seconds=now.second, microseconds=now.microsecond)
    d2 = timedelta(minutes=1)
    nextMinute = now - d1 + d2

    while True:
        if datetime.now(timezone.utc) > nextMinute:
            return
        time.sleep(.5)

    # nextMinuteRounded = datetime(years = nextMinuteActual.year,
    #                              month = nextMinuteActual.month,
    #                              day = nextMinuteActual.day,
    #                              hour = nextMinuteActual.)
    

#check if valid stock name by checking if there is a latest quote for it
def checkValidStock(api_key, secret_key, symbol):
    client = StockHistoricalDataClient(api_key, secret_key)
    request = StockLatestQuoteRequest(symbol_or_symbols=symbol)

    try:
        res = client.get_stock_latest_quote(request)
        return True
    except APIError as err:
        return False



if __name__ == '__main__':
    isMarketOpen(datetime.now(timezone.utc))
    #dto = datetime.fromisoformat('2024-04-04T13:45:23Z')
    #isMarketOpen(dto)