import quantstats as qs
import datetime as dt
import tkinter as tk
from classes import Portfoliolist, Portfolio, Entry
import yfinance as yf
import webbrowser
import os

ticker = "AAPL"
start = dt.date(2020,1,1)
end = dt.date.today()
sma = 200

myentry = Entry(ticker = ticker, id = 0)
gtaa, bh, first_date = myentry.calculation(start = start, end = end, sma = sma)
print(gtaa)