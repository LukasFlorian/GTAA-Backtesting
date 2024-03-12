"""
__attribute: private attribute (access only from inside class)
_attribute: protected attribute (access from inside class and subclass)
__attribute and @property: read-only attribute
"""


import yfinance as yf
import datetime as dt
from dateutil import relativedelta as rd
import quantstats as qs
import pandas as pd
#import pandas as pd

class Entry:
    def __init__(self, ticker: str, id: int) -> None:
        """an entry in a portfolio. Assumes that the ticker is valid, must have an id to identify itself in the portfolio

        Args:
            ticker (str): valid security ticker accessible on yfinance
            id (int): id in portfolio
        """
        self.__id = id
        self.__ticker = ticker
        self.__name = yf.Ticker(ticker).info["longName"]
        #self.__history = yf.Ticker(ticker).history(period = "max")["Close"]

    
    @property
    def ticker(self) -> str:
        return self.__ticker
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def id(self) -> int:
        return self.__id
    
    def set_id(self, new: int) -> None:
        self.__id = new
    
    def set_ticker(self, newticker: str) -> None:
        self.__ticker = newticker
        self.update_name()
        #self.update_history()
    
    def update_name(self) -> None:
        self.__name = yf.Ticker(self.__ticker).info["longName"]
    
    def calculation(self, start: dt.date, end: dt.date, sma: int) -> list:
        """used for performance calculation of the stock
        
        Args:
            start (dt.datetime): start date for calculation
            end (dt.datetime): end date for calculation
            sma (int): numbers of days for the SMA
        """
        history = yf.Ticker(self.ticker).history(period = "max").Close
        #history: pandas series, contains only trading days, date index is timezone aware
        #make timezone unaware (so can be compared to unaware dt.datetime start and end):
        #get series index:
        dates = list(history.index.values)
        #convert from pandas timstamp to dt.datetime object, make timezone unaware:
        dates = [pd.Timestamp(date).to_pydatetime().replace(tzinfo = None).date() for date in dates]
        #change history series index:
        history.index = dates

        factors = [quote for quote in history]
        q0 = factors[0]
        #norm to start at Factor 1
        factors = [quote/q0 for quote in factors]
        #now converting history to dataframe:
        history = history.to_frame()
        history["SMA"] = history["Close"].rolling(window = sma).mean()
        print(history)
        print(type(history.iloc[0].name))
        #index to start calculation at
        index = 0
        while history.iloc[index].name < start:
            index += 1
        history = history.iloc[index:]


        index = 0
        investment = 1
        bh_investment = 1
        previous = history.iloc[0]["Close"]
        dates = []
        gtaa = []
        bh = []
        curdate = start
        #indicator whether the decision for the current period is to buy or not
        cur_decision = bool(history.iloc[index]["SMA"] < history.iloc[index]["Close"])
        #date for the next buying/selling decision
        next_decision = start + rd.relativedelta(months = 1)
        while curdate <= end:
            if curdate == next_decision:    #check if new period begins
                cur_decision = bool(history.iloc[index]["SMA"] < history.iloc[index]["Close"])
                next_decision += rd.relativedelta(months = 1)

            if index < len(history):
                if cur_decision is True:            
                    if curdate < history.iloc[index].name:
                        #making sure no dates are missing in investment performance
                        #non-trading days would otherwise be missing
                        dates.append(curdate)
                        gtaa.append(investment)
                        bh.append(bh_investment)
                        curdate += dt.timedelta(days = 1)
                    else:
                        dates.append(curdate)
                        #currently buying -> invesment changes
                        investment *= history.iloc[index]["Close"]/previous
                        bh_investment *= history.iloc[index]["Close"]/previous
                        gtaa.append(investment)
                        bh.append(bh_investment)
                        previous = history.iloc[index]["Close"]
                        index += 1
                        curdate += dt.timedelta(days = 1)
                        
                if cur_decision is False:            
                    if curdate < history.iloc[index].name:
                        #making sure no dates are missing in investment performance
                        #non-trading days would otherwise be missing
                        dates.append(curdate)
                        gtaa.append(investment)
                        bh.append(bh_investment)
                        curdate += dt.timedelta(days = 1)
                    else:
                        dates.append(curdate)
                        #currently not buying -> investment not changing
                        gtaa.append(investment)
                        bh_investment *= history.iloc[index]["Close"]/previous
                        bh.append(bh_investment)
                        previous = history.iloc[index]["Close"]
                        index += 1
                        curdate += dt.timedelta(days = 1)
            else:
                #filling up rest of days until end day
                dates.append(curdate)
                gtaa.append(investment)
                bh.append(bh_investment)
                curdate += dt.timedelta(days = 1)
        dates = [pd.Timestamp(date) for date in dates]
        gtaa = pd.Series(data = gtaa, index = dates, name = "GTAA")
        bh = pd.Series(data = bh, index = dates, name = "Buy & Hold")
        return gtaa, bh



class Portfolio:
    def __init__(self, entries: list, average: int):
        self.__entries = {i: Entry(entries[i][0], i) for i in range(len(entries))}  #tickers must be unique
        self.__weights = {i: entries[i][1] for i in range(len(entries))}
        self.__num_entries = len(entries)-1
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
    
    def relative_calculation(self, start: dt.date, end: dt.date) -> list:
        gtaa_list, bh_list = [], []
        first_date = start
        last_date = end
        for entry_id in self.entries:
            gtaa, bh = self.entries[entry_id].calculation(start = start, end = end, sma = self.average)
            first_date = max(first_date, gtaa.index[0].to_pydatetime().date())
            last_date = min(last_date, gtaa.index[-1].to_pydatetime().date())
            gtaa_list.append(gtaa)
            bh_list.append(bh)
        gtaa = gtaa_list[0][first_date:last_date]*self.weights[0]
        bh = bh_list[0][first_date:last_date]*self.weights[0]
        for index in range(1, len(gtaa_list)):
            next_gtaa = gtaa_list[index]
            next_bh = bh_list[index]
            next_gtaa = next_gtaa[first_date:last_date]
            next_bh = next_bh[first_date:last_date]
            gtaa += next_gtaa*self.weights[index]
            bh += next_bh*self.weights[index]
        return gtaa, bh


class Portfoliolist:
    def __init__(self, portfolios: list):
        self.__portfolios = {name: portfolio for name, portfolio in portfolios}
    
    @property
    def portfolios(self) -> dict:
        return self.__portfolios
    
    def addPortfolio(self, portfolio: Portfolio, name: str) -> None:
        self.__portfolios[name] = portfolio
    
    def performCalulation(self, name: str, start: dt.date, end: dt.date) -> None:
        gtaa, bh = self.portfolios[name].relative_calculation(start, end)
        return gtaa, bh