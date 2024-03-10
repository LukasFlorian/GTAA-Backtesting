#%matplotlib inline
import yfinance as yf
import quantstats as qs
import pandas as pd
import sqlite3 as sql
import streamlit as st
"""
# extend pandas functionality with metrics, etc.
qs.extend_pandas()

# fetch the daily returns for a stock
stock = qs.utils.download_returns('META')

# show sharpe ratio
print(qs.stats.sharpe(stock))

# or using extend_pandas() :)
print(stock.sharpe())
qs.reports.html(stock, "SPY", output = "report.html")


historic_data = yf.Ticker("META").history(period = "max")
print(type(historic_data))
print(historic_data.index[0]) #oldest
print(historic_data.index[-1]) #newest
print(historic_data.shape) #(rows, cols)
"""

def openConnection() -> tuple:
    """used to open database connection, informs about status of connection (successful or not)

    Returns:
        cur, conn: cursor for and connection to database
    """
    database = "📈GTAA-Backtesting/new_approach/gtaa_database.db"
    try:
        conn = sql.connect(database)
        print("Database Sqlite3.db formed.") 
    except:
        raise Exception("Database Sqlite3.db not formed.")
        #print("Database Sqlite3.db not formed.")
        
    cur = conn.cursor()
    return cur, conn
"""
cur, conn = openConnection()
test = cur.execute("select * from Historic where ticker = \"META\"")
test = test.fetchall()
print(test)
entry = cur.execute("select ticker from Stocks where ticker = \"META\"").fetchall()
print(type(entry[0]))
"""

stock = yf.Ticker("META")
name = stock.info["longName"]

print(stock.info)
history = stock.history(period = "max")
oldest_date = history.index[0]
newest_date = history.index[-1]
print(history)