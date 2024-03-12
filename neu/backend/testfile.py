#%matplotlib inline
import yfinance as yf
import quantstats as qs
import pandas as pd
import sqlite3 as sql
import streamlit as st
import datetime as dt
from dateutil import relativedelta as rd
import numpy as np
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

from classes import Portfolio
"""test = Portfolio(entries = [("^GSPC", 0.2), ("EFA", 0.2), ("GLD", 0.2), ("O", 0.2), ("IEF", 0.2)], average = 200, name = "mytest")
start = dt.datetime(year = 2024, month = 1, day = 1)
#end = dt.datetime(year = 2021, month = 3, day = 1)
end = dt.datetime.now()

gtaa = test.gtaa_relative_calculation(start, end)
b_h = test.buy_and_hold_relative_calculation(start, end)
#print("gtaa:", gtaa[-1][1])
#print("b & h:", b_h[-1][1])
print(gtaa)"""
"""
stock = qs.utils.download_returns('META')
weights = [0.25, 0.25, 0.25, 0.25]
portfolio = qs.utils.download_returns('AAPL')*weights[0] + qs.utils.download_returns('TSLA')*weights[1] + qs.utils.download_returns('META')*weights[2] + qs.utils.download_returns('AMD')*weights[3]
qs.reports.full(portfolio, benchmark = "sp500")"""
def listToDf(list: list) -> pd.DataFrame:
    dictionary = {x[0]: [x[1]-1] for x in list}
    dataframe = pd.DataFrame.from_dict(dictionary, columns=["Returns"], orient='index').rename_axis("Date")
    #dataframe = pd.DataFrame(list, columns = ["Date", "Return"])
    return dataframe

"""portfolio = Portfolio(entries = [("META", 1)], average = 200, name = "mine")
earliest = portfolio.get_earliest()
gtaa = portfolio.gtaa_relative_calculation(start=earliest, end = dt.datetime.now())
bh = portfolio.buy_and_hold_relative_calculation(start=earliest, end = dt.datetime.now())
gtaa, bh = listToDf(gtaa).Returns, listToDf(bh).Returns
print(gtaa)
print(bh)"""
start = dt.datetime(2020,1,1)
end = dt.datetime.now()
average = 200
history = qs.utils.download_returns("META", period = "max").loc[start - dt.timedelta(days = average):end]
print(history)
#qs.reports.html(gtaa, title = portfolio.name, output = portfolio.name + ".html", download_filename = "profit.html")
"""start_amount = 100000

np.random.seed(8)
win_loss_df = pd.DataFrame(
    np.random.choice([1000, -1000], 543),
    index=pd.date_range("2020-01-01", "2022-01-30", freq="B"),
    columns=["win_loss_amount"]
)
win_loss_df["total_profit"] = win_loss_df.win_loss_amount.cumsum() + start_amount

profit = win_loss_df.total_profit

# Save to image file, this image can also be seen in full report.
qs.plots.yearly_returns(profit, savefig='yearly_return.png')

print(f'montly returns:\n{qs.stats.monthly_returns(profit)}')
print(f'sharpe ratio: {qs.stats.sharpe(profit)}')
print(f'max markdown: {qs.stats.max_drawdown(profit)}')

# Print full report in html.
qs.reports.html(profit, title='ABC', output='profit.html', download_filename='profit.html')"""