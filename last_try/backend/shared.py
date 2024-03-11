import yfinance as yf
from backend.classes import Portfoliolist

global portfolios
portfolios = Portfoliolist([])

relative_prefix = "GTAA_Backtesting/"
def add_prefix(filename: str) -> str:
    return relative_prefix + filename + ".py"

def checkyFinance(ticker: str):
    """to check if a given ticker exists on yahooFinance

    Args:
        ticker (str): ticker to check

    Returns:
        bool: True if ticker exists, otherwise False
    """
    try:
        name = yf.Ticker(ticker).info["longName"]
    except:
        return False
    return True