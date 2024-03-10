"""
__attribute: private attribute (access only from inside class)
_attribute: protected attribute (access from inside class and subclass)
__attribute and @property: read-only attribute
"""

import sqlite3 as sql
import yfinance as yf
import datetime as dt

class Stock:
    def __init__(self, ticker: str, name: str) -> None:
        self.__ticker = ticker
        self.__name = name
    
    @property
    def ticker(self) -> str:
        return self.__ticker
    
    @property
    def name(self) -> str:
        return self.__name
    
    def _set_ticker(self, newticker: str) -> None:
        self.__ticker = newticker
    
    def _set_name(self, newname: str) -> None:
        self.__name = newname

class Entry(Stock):
    def __init__(self, ticker: str, name: str, oldest: dt.datetime, newest: dt.datetime) -> None:
        super().__init__(ticker, name)
        self.oldest = oldest
        self.newest = newest

class DB:
    """database connection class to use database
    """
    def __init__(self) -> None:
        try:
            conn = sql.connect("📈GTAA-Backtesting/new_approach/gtaa_database.db")
            print("Database formed.")
        except:
            raise Exception("Database not formed.")
        self.__conn = conn
        self.__cur = conn.cursor()
    
    def initialize_database(self) -> None:
        """initial creation of database with stocks table for stock ticker and name and historic table with historic prices for stocks on any given date
        """
        self.__cur.execute("CREATE TABLE Stocks (ticker TEXT PRIMARY KEY, name TEXT NOT NULL, first_quote TEXT, last_quote TEXT, number_quotes INT)")
        self.__cur.execute("CREATE TABLE Historic (ticker TEXT NOT NULL, date TEXT NOT NULL, quote INT NOT NULL, ttm_sma INT NOT NULL, two_day_sma INT NOT NULL, ten_month_sma INT NOT NULL, six_month_sma INT NOT NULL, five_month_sma INT NOT NULL, three_month_sma INT NOT NULL, two_month_sma INT NOT NULL, PRIMARY KEY (ticker, date), FOREIGN KEY (ticker) REFERENCES Stocks(ticker))")
    
    def dropAll(self) -> None:
        """used to delete all database tables in case it needs to be re-initialized
        """
        self.__cur.execute("DROP TABLE Stocks")
        self.__cur.execute("DROP TABLE Historic")
    
    def close(self) -> None:
        """close the database connection to save resources
        """
        self.__conn.close()
        self = None

    def addStock(self, stock: Entry, earliest, last) -> None:
        self.__cur.execute("INSERT INTO Stocks VALUES (\'" + stock.ticker + "\', \'" + stock.name + "\', \"" + stock.oldest + "\", \"" + stock.newest + "\")")
        

    def checkStock(self, ticker: str) -> None:
        """check if a stock is in the database

        Args:
            ticker (str): _description_

        Returns:
            None: -
        """
        entry = self.__cur.execute("select ticker from Stocks where ticker = \"" + ticker + "\"").fetchall()
        return bool(len(entry))
    
    def getKnownStocks(self) -> list:
        """function to get a list of all stocks in the database

        Returns:
            list: list of Entry objects for stocks in the database
        """
        entries = self.__cur.execute("select * from Stocks").fetchall()
        entries = [Entry(entry[0], entry[1], entry[2], entry[3]) for entry in entries]
        return entries
        

class Portfolio:
    pass