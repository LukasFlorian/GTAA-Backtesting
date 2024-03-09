#%matplotlib inline
import yfinance as yf
import quantstats as qs
import pandas as pd

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
print(historic_data.index[0])
print(historic_data.index[-1])