import pandas_market_calendars as mcal
from datetime import datetime, timedelta, timezone
import pandas


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


if __name__ == '__main__':
    isMarketOpen(datetime.now(timezone.utc))
    #dto = datetime.fromisoformat('2024-04-04T13:45:23Z')
    #isMarketOpen(dto)