"""
__attribute: private attribute (access only from inside class)
_attribute: protected attribute (access from inside class and subclass)

"""

import sqlite3 as sql

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

class DB_Connection:
    def __init__(self) -> None:
        try:
            conn = sql.connect("/workspaces/Laufzeitoptimierung/📈GTAA-Backtesting/data/gtaa_database.db")
            print("Database Sqlite3.db formed.") 
        except:
            raise Exception("Database Sqlite3.db not formed.")
            #print("Database Sqlite3.db not formed.")
            
        cur = conn.cursor()
        self.__cur = cur
        self.__conn = conn
    
    def addStock(self, stock: Stock):
        cur.execute("INSERT INTO Stocks VALUES (\'" + stock.ticker + "\', \'" + stock.name + "\')")
        