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
        history = yf.download(self.ticker, start=start - dt.timedelta(days = average), end=end)
        first_valid = 0
        while history.iloc[first_valid].name.to_pydatetime() < start:
            first_valid += 1
        sma = history[first_valid - average:first_valid]["Close"].mean()
        last_date = start
        last_weight = weight
        daily = []
        if sma < history.iloc[first_valid]["Close"]:
            if history.iloc[first_valid].name.to_pydatetime() > start:
                daily.append((start, weight))
            for day in range(first_valid, history.shape[0]):
                while history.iloc[day].name.to_pydatetime() - last_date > dt.timedelta(days = 1):
                    last_date += dt.timedelta(days = 1)
                    daily.append((last_date, last_weight))
                last_date = history.iloc[day].name.to_pydatetime()
                last_weight = history.iloc[day]["Close"]/history.iloc[first_valid]["Close"]*weight
                daily.append((last_date, last_weight))
            while end - last_date > dt.timedelta(days = 1):
                last_date += dt.timedelta(days = 1)
                daily.append((last_date, last_weight))
        else:
            while start < end:
                daily.append((start, weight))
                start += dt.timedelta(days = 1)
            #daily = [(history.index[day], weight) for day in range(first_valid, history.shape[0])]
        return daily

    def buy_and_hold(self, start: dt.datetime, end: dt.datetime, weight: int, average: int) -> list:
        history = yf.download(self.ticker, start=start, end=end)
        last_date = start
        last_weight = weight
        daily = []
        if history.iloc[0].name.to_pydatetime() > start:
            daily.append((start, weight))
        for day in range(history.shape[0]):
            while history.iloc[day].name.to_pydatetime() - last_date > dt.timedelta(days = 1):
                last_date += dt.timedelta(days = 1)
                daily.append((last_date, last_weight))
            last_date = history.iloc[day].name.to_pydatetime()
            last_weight = history.iloc[day]["Close"]/history.iloc[0]["Close"]*weight
            daily.append((last_date, last_weight))
        while end - last_date > dt.timedelta(days = 1):
            last_date += dt.timedelta(days = 1)
            daily.append((last_date, last_weight))
        return daily
        
        
        
        

class Portfolio:
    def __init__(self, entries: list, average: int, name: str):
        self.__entries = {i: Entry(entries[i][0], i) for i in range(len(entries))}  #tickers must be unique
        self.__weights = {i: entries[i][1] for i in range(len(entries))}
        self.__num_entries = len(entries)-1
        self.__average = average
        self.__name = name
        self.__id = None
    
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
    @property
    def name(self) -> str:
        return self.__name
    @property
    def id(self) -> int:
        return self.__id
    
    def set_id(self, new: int) -> None:
        self.__id = new

    def changeWeight(self, id: int, new: float) -> None:
        self.__weights[id] = new
    
    def set_average(self, new: int) -> None:
        self.__average = new
    
    def set_num_entries(self, new: int) -> None:
        self.__num_entries = new
    
    def set_name(self, new: str) -> None:
        self.__name = new
    
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
    
    def gtaa_relative_calculation(self, start: dt.datetime, end: dt.datetime) -> list:
        cumulative = []
        value = 1
        while start < end:
            current_end = start + rd.relativedelta(months = 1)
            if (end - current_end)/dt.timedelta(days = 1) < 0:
                current_end = end
            performance = {}
            for id in range(self.num_entries):
                performance[id] = self.entries[id].relative_calculation(start, current_end, self.weights[id]*value, self.average)
            number_days = len(performance[0])
            first_date = start
            for i in range(number_days):
                day = [first_date, 0]
                for id in performance:
                    day[1] += performance[id][i][1]
                cumulative.append(day)
                first_date += dt.timedelta(days = 1)
            value = cumulative[-1][1]
            start += rd.relativedelta(months = 1)
        return cumulative
    
    def buy_and_hold_relative_calculation(self, start: dt.datetime, end: dt.datetime) -> list:
        cumulative = []
        performance = {}
        for id in range(self.num_entries):
            performance[id] = self.entries[id].buy_and_hold(start, end, self.weights[id], self.average)
        number_days = len(performance[0])
        for i in range(number_days):
            day = [start, 0]
            for id in performance:
                day[1] += performance[id][i][1]
            cumulative.append(day)
            start += dt.timedelta(days = 1)
        return cumulative




class Portfoliolist:
    def __init__(self, portfolios: list):
        self.__portfolios = {i: portfolios[i] for i in range(len(portfolios))}
        self.__num_portfolios = len(portfolios)-1
    
    @property
    def portfolios(self) -> dict:
        return self.__portfolios
    @property
    def num_portfolios(self) -> int:
        return self.__num_portfolios
    
    def set_num_portfolios(self, new: int) -> None:
        self.__num_portfolios = new
    
    def addPortfolio(self, portfolio: Portfolio) -> None:
        portfolio.set_id(self.num_portfolios + 1)
        self.__portfolios[self.num_portfolios + 1] = portfolio
        self.set_num_portfolios(self.num_portfolios + 1)
    
    def deletePortfolio(self, id: int) -> None:
        for i in range(id+1, self.num_portfolios):
            self.__portfolios[i].set_id(i-1)
            self.__portfolios[i-1] = self.__portfolios[i]
        del self.__portfolios[self.num_portfolios]
        self.set_num_portfolios(self.num_portfolios - 1)