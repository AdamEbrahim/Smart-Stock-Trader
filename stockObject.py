from enum import Enum
from alpaca.data.timeframe import TimeFrame
import threading
from collections import deque

class dataType(Enum):
    BAR = "Bar"
    TRADE = "Trade"
    QUOTE = "Quote"


class stockObject:

    #timeframeUnit is an enum alpaca.data.timeframe.TimeFrameUnit
    def __init__(self, symbol, timeframeAmount, timeframeUnit):
        self.symbol = symbol

        self.model = dataType.TRADE
        
        #need a lock for data as web socket thread and main thread (when initializing historical data) may write to data at same time
        self.data = deque()
        self.lock = threading.Lock()

        self.timeInterval = TimeFrame(timeframeAmount, timeframeUnit)

        self.initHistoricData()


    #timeframeUnit is an enum alpaca.data.timeframe.TimeFrameUnit
    def changeTimeInterval(self, timeframeAmount, timeframeUnit):
        del self.timeInterval
        self.timeInterval = TimeFrame(timeframeAmount, timeframeUnit)
        print("changed time interval")
        self.initHistoricData()


    def initHistoricData(self):
        self.lock.acquire()
        print("hi")

        self.lock.release()