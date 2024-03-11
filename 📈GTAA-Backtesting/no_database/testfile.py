#%matplotlib inline
import yfinance as yf
import quantstats as qs
import pandas as pd
import sqlite3 as sql
import streamlit as st
import datetime as dt
from dateutil import relativedelta as rd
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

"""
stock = yf.Ticker("META")
name = stock.info["longName"]

print(stock.info)
history = stock.history(period = "max")
oldest_date = history.index[0]
newest_date = history.index[-1]
print(type(newest_date.to_pydatetime()))"""
"""print(history["Close"])

print(yf.download("AAPL", start=dt.datetime(year = 2021, month = 1, day = 1), end=dt.datetime(year = 2022, month = 1, day = 1)))
test = dt.datetime(year = 2022, month = 1, day = 1)
print(dt.datetime(year = 2022, month = 1, day = 1))
print(test - rd.relativedelta(years = 1))"""
#print(dt.datetime(year=2022, month=2, day=1) > dt.datetime(year=2022, month=2, day=3))

from classes import Entry, Portfolio
test = Portfolio(entries = [("^GSPC", 0.2), ("EFA", 0.2), ("GLD", 0.2), ("O", 0.2), ("IEF", 0.2)], average = 200, name = "mytest")
start = dt.datetime(year = 2005, month = 1, day = 1)
#end = dt.datetime(year = 2021, month = 3, day = 1)
end = dt.datetime.now()

gtaa = test.gtaa_relative_calculation(start, end)
b_h = test.buy_and_hold_relative_calculation(start, end)
print("gtaa:", gtaa[-1][1])
print("b & h:", b_h[-1][1])