"""
__attribute: private attribute (access only from inside class)
_attribute: protected attribute (access from inside class and subclass)
__attribute and @property: read-only attribute
"""


import yfinance as yf
import datetime as dt
from dateutil import relativedelta as rd

class Entry:
    def __init__(self, ticker: str, id: int) -> None:
        self.id = id
        self.__ticker = ticker
        self.__name = yf.Ticker(ticker).info["longName"]
        #self.__history = yf.Ticker(ticker).history(period = "max")["Close"]

    
    @property
    def ticker(self) -> str:
        return self.__ticker
    
    @property
    def name(self) -> str:
        return self.__name
    
    def set_id(self, new: int) -> None:
        self.id = new
    
    def get_id(self) -> int:
        return self.id
    
    def set_ticker(self, newticker: str) -> None:
        self.__ticker = newticker
        self.update_name()
        self.update_history()
    
    def update_name(self) -> None:
        self.__name = yf.Ticker(self.__ticker).info["longName"]
    
    """
    def update_history(self) -> None:
        self.__history = yf.Ticker(self.ticker).history(period = "max")"""
        
    def relative_calculation(self, start: dt.datetime, end: dt.datetime, weight: int, average: int)
        history = yf.download(self.ticker, start=start - rd.relativedelta(days = average * 14), end=end)["Close"]
        first_valid = 0
        while history.index[first_valid] < start:
            first_valid += 1
        sma = history[first_valid - average:first_valid].mean()
        if sma < history[first_valid]:
            daily = []
            for day in range(first_valid, history.shape[0]):
                daily.append((history.index[day], history[day]/history[first_valid]*weight))
        else:
            daily = [(history.index[day], weight) for day in range(first_valid, history.shape[0])]
        return daily

    def absolute_calculation(self, start: dt.datetime, end: dt.datetime, weight: int, average: int, investment: float)
        relative = self.relative_calculation(start, end, weight, average)
        absolute = [(day, weight * investment) for day, weight in relative]
        return relative, absolute
        
        
        
        

class Portfolio:
    def __init__(self, entries: list, fee: float, commission: float, sma: int, initial = None, monthly = None):
        self.__entries = {i: Entry(entries[i][0], i) for i in range(len(entries))}  #tickers must be unique
        self.__weights = {i: entries[1] for i in range(len(entries))}
        self.__num_entries = len(entries)
        self.__initial = initial
        self.__monthly = monthly
    
    @property
    def entries(self) -> dict:
        return self.__entries
    @property
    def weights(self) -> dict:
        return self.__weights
    @property
    def num_entries(self) -> int:
        return self.__num_entries

    def changeWeight(self, id: int, new: float) -> None:
        self.__weights[id] = new
    
    def set_num_entries(self, new: int) -> None:
        self.__num_entries = new
    
    def deleteEntry(self, id: int) -> None:
        for i in range(id+1, self.num_entries):
            self.__entries[i].set_id(i-1)
            self.__entries[i-1] = self.__entries[i]
            self.changeWeight(i-1, self.__weights[i])
        del self.__entries[self.num_entries]
        del self.__weights[self.num_entries]
        self.set_num_entries(self.num_entries - 1)
    
    def add_entry(self, ticker: str, weight: float) -> None:
        self.__entries[self.num_entries + 1] = Entry(ticker, )
    
    def change_entry_ticker(self, id, newticker: str):
        self.__entries[id].set_ticker(newticker)
    
    def calculation(self, )