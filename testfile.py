import quantstats as qs
import datetime as dt
from dateutil import relativedelta as rd
import pandas as pd
from classes import Portfoliolist
from tkinter import *

ticker1 = "^GSPC"
ticker2 = "AAPL"
start = dt.date(1900, 1, 1)
end = dt.date.today()
sma = 200

"""
mytest1 = Entry(ticker = ticker1, id = 0)
mytest2 = Entry(ticker = ticker2, id = 0)
gtaa1, bh1 = mytest1.calculation(start=start, end = end, sma=sma)
gtaa2, bh2 = mytest2.calculation(start=start, end = end, sma=sma)
gtaa = 0.7*gtaa1+0.3*gtaa2
bh = 0.7*bh1+0.3*bh2
"""
"""
myportfolio = MyPortfolio([(ticker1, 0.9), (ticker2, 0.1)], average=sma, name="myPortfolio")
gtaa, bh = myportfolio.relative_calculation(start=start, end=end)

qs.reports.html(returns = gtaa, benchmark=bh, title = "metatest", output='local/metatest.html')
"""

def ticker_section(startrow: int) -> None:
    Label(root, text = "Provide a security ticker and the weight it should have in your portfolio:").grid(row = startrow, column = 1)
    Label(root, text = "Ticker:").grid(row = startrow, column = 2)
    Label(root, text = "Weight (Decimal percentage between 0 and 100):").grid(row = startrow, column = 3)
    ticker = Entry(root)
    ticker.grid(row = startrow + 1, column = 2)
    weight = Entry(root)
    weight.grid(row = startrow + 1, column = 3)
    tickerlist.append(ticker)
    weightlist.append(weight)
    
def createTickerSection(tickercount: int) -> None:
    if tickercount <= 0:
        Label(root, text = "Please make sure the number of tickers is positive.").grid(row = 4, column = 1)
    else:
        for i in range(tickercount):
            ticker_section(startrow = 4 + 2*i)
        createPortfolioSection()

root = Tk()
root.title("GTAA Backtesting Tool by Lukas Florian Richter & Nemanja Cerovac")    
Label(root, text = "Here you can backtest your GTAA strategies with custom securities and SMAs to use.").grid(row = 0, column = 0, columnspan=4)

#new portfolio section
Label(root, text = "Create a new strategy in this section:").grid(row = 1, column = 0)
Label(root, text = "Please name your strategy here:").grid(row = 1, column = 1)
name = Entry(root)
name.grid(row = 1, column = 2)
Label(root, text = "Insert the number of days used for the SMA:").grid(row = 2, column = 1)
sma = Entry(root)
sma.grid(row = 2, column = 2)
Label(root, text = "How many tickers should your portfolio have?").grid(row = 3, column = 1)
tickerinput = Entry(root)
tickerinput.grid(row = 3, column = 2)
global tickerlist, weightlist, ready
tickerlist, weightlist = [], []


def get_numberinput(widget: Entry) -> int:
    try:
        return int(widget.get())
    except:
        return 0

Button(root, text = "Enter Securities", command= lambda: createTickerSection(get_numberinput(tickerinput))).grid(row = 3, column = 3)
#lambda because otherwise tkinter would run the command immediately after creating the button

def checkRequirements() -> tuple:
    average = get_numberinput(sma)
    if average is 0:
        pass
    tickers = [entry.get() for entry in tickerlist]
    weights = [entry.get() for entry in weightlist]
portfolios = Portfoliolist([])

def createPortfolioSection(tickercount: int) -> None:
    tickercount = int(tickerinput.get())
    Button(root, text = "Reset input fields", command = root.destroy).grid(row = 4 + tickercount*2)
    Button(root, text = "Create Strategy", command = lambda: checkRequirements(name, sma, tickerinput))
    


root.mainloop()