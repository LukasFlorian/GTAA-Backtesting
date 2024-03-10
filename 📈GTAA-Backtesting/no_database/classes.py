"""
__attribute: private attribute (access only from inside class)
_attribute: protected attribute (access from inside class and subclass)
__attribute and @property: read-only attribute
"""


import yfinance as yf
import datetime as dt
from dateutil import relativedelta as rd
#import pandas as pd

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
        #self.update_history()
    
    def update_name(self) -> None:
        self.__name = yf.Ticker(self.__ticker).info["longName"]
    
    """
    def update_history(self) -> None:
        self.__history = yf.Ticker(self.ticker).history(period = "max")"""
        
    def relative_calculation(self, start: dt.datetime, end: dt.datetime, weight: int, average: int) -> list:
        history = yf.download(self.ticker, start=start - dt.timedelta(days = average * 14), end=end)["Close"]
        first_valid = 0
        while history.index[first_valid].to_pydatetime() < start:
            first_valid += 1
        sma = history[first_valid - average:first_valid].mean()
        last_date = start
        last_weight = weight
        daily = []
        if sma < history[first_valid]:
            if history.index[first_valid].to_pydatetime() > start:
                daily.append((start, weight))
            for day in range(first_valid, history.shape[0]):
                while history.index[day].to_pydatetime() - last_date > dt.timedelta(days = 1):
                    last_date += dt.timedelta(days = 1)
                    daily.append((last_date, last_weight))
                last_date = history.index[day].to_pydatetime()
                last_weight = history[day]/history[first_valid]*weight
                daily.append((last_date, last_weight))
        else:
            while start < end:
                daily.append((start, weight))
                start += dt.timedelta(days = 1)
            #daily = [(history.index[day], weight) for day in range(first_valid, history.shape[0])]
        return daily

    """def absolute_calculation(self, start: dt.datetime, end: dt.datetime, weight: int, average: int, investment: float) -> tuple:
        relative = self.relative_calculation(start, end, weight, average)
        absolute = [(day, weight * investment) for day, weight in relative]
        return relative, absolute"""
        
        
        
        

class Portfolio:
    def __init__(self, entries: list, fee: float, commission: float, average: int, initial = None, monthly = None):
        self.__entries = {i: Entry(entries[i][0], i) for i in range(len(entries))}  #tickers must be unique
        self.__weights = {i: entries[1] for i in range(len(entries))}
        self.__num_entries = len(entries)
        self.__initial = initial
        self.__monthly = monthly
        self.__average = average
    
    @property
    def entries(self) -> dict:
        return self.__entries
    @property
    def weights(self) -> dict:
        return self.__weights
    @property
    def num_entries(self) -> int:
        return self.__num_entries
    
    @property
    def average(self) -> int:
        return self.__average

    def changeWeight(self, id: int, new: float) -> None:
        self.__weights[id] = new
    
    def set_average(self, new: int) -> None:
        self.__average = new
    
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
        self.__entries[self.num_entries + 1] = Entry(ticker, self.num_entries + 1)
        self.__weights[self.num_entries + 1] = weight
        self.set_num_entries(self.num_entries+1)
    
    def change_entry_ticker(self, id, newticker: str) -> None:
        self.__entries[id].set_ticker(newticker)
    
    def relative_calculation(self, start: dt.datetime, end: dt.datetime) -> list:
        cumulative = []
        value = 1
        while start < end:
            current_end = start + dt.timedelta(months=1)
            if (end - current_end)/dt.timedelta(days = 1) < 0:
                current_end = end
            performance = {}
            for id in range(self.num_entries):
                performance[id] = self.entries[id].relative_calculation(start, current_end, self.weights[id]*value, self.average)
            number_days = len(performance[0])
            for i in range(number_days):
                day = (start, 0)
                for id in performance:
                    day[1] += performance[id][i]
                cumulative.append(day)
                start += dt.timedelta(days = 1)
            value = cumulative[-1][1]
        return cumulative