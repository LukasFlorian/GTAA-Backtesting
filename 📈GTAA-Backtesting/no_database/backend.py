#%matplotlib inline
import yfinance as yf
import quantstats as qs
import pandas as pd
import streamlit as st
from classes import Portfolio, Entry

def checkyFinance(ticker):
    """to check if a given ticker exists on yahooFinance

    Args:
        ticker (str): ticker to check

    Returns:
        bool: True if ticker exists, otherwise False
    """
    ticker = yf.Ticker(ticker)
    try:
        info = ticker.info
        return True
    except:
        return False

"""
Stocks table:
1. ticker, name, most recent quote

- insert new stock
- determine if update is necessary
- update


1. only ticker, date, quote in database
2. convert to pandas dataframe
3. determine earliest date
4. 



Only stock new if:
- weight change

Whole portfolio new if:
- ticker change
- date change
- average change
- treasuries yes/no
"""