import quantstats as qs
import datetime as dt
import pandas as pd
from classes import *


ticker = "META"
start = dt.date(2020, 1, 1)
end = dt.date.today()
print(type(start))
sma = 200
history = yf.Ticker(ticker).history(period = "max").Close
#history: pandas series, contains only trading days, date index is timezone aware
#make timezone unaware (so can be compared to unaware dt.datetime start and end):
#get series index:
dates = list(history.index.values)
#convert from pandas timstamp to dt.datetime object, make timezone unaware:
dates = [pd.Timestamp(date).to_pydatetime().date() for date in dates]
print(type(dates[0]))
#change history series index:
history.index = dates
history = history.iloc[start : end]

factors = [quote for quote in history]
start = factors[0]
#norm to start at Factor 1
factors = [quote/start for quote in factors]
#now converting history to dataframe:
history = history.to_frame()
history.insert(1, "Factor", factors, True)
for index in range(1, len(factors)):
    factors[index] *= factors[index-1]
#factors now contains cumulative returns
# -> can be used to get simple moving average (sma)
#adding simple moving average column:
history["SMA"] = history["Factor"].rolling(window = sma).mean()
print(history)