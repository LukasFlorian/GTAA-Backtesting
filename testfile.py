import quantstats as qs
import datetime as dt
import pandas as pd
from classes import Portfoliolist, Portfolio
from tkinter import *
import yfinance as yf

"""
ticker1 = "^GSPC"
ticker2 = "AAPL"
start = dt.date(1900, 1, 1)
end = dt.date.today()
sma = 200
"""

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
def checkyFinance(ticker: str):
    try:
        name = yf.Ticker(ticker).info["longName"]
    except:
        return False
    return True

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

def get_numberinput(widget: Entry) -> int:
    try:
        return int(widget.get())
    except:
        return -1
    
def checkRequirements(tickercount: int) -> tuple:
    average = get_numberinput(sma)
    if average < 2:
        Label(root, text = "Make sure the SMA is an integer of at least 2.").grid(row = 5 + (tickercount-1)*2, column = 1)
    elif name == "":
        Label(root, text = "Make sure to give your strategy a name.").grid(row = 5 + (tickercount-1)*2, column = 1)
    else:
        tickers = [entry.get() for entry in tickerlist]
        weights = [get_numberinput(entry) for entry in weightlist]
        for ticker in tickers:
            valid = checkyFinance(ticker)
            if valid is False:
                Label(root, text = "The ticker " +  ticker + " is not a valid ticker on yahooFinance.").grid(row = 5 + (tickercount-1)*2, column = 1)
                break
        if valid is True:
            for weight in weights:
                if weight < 0 or weight > 100:
                    Label(root, text = "Please make sure all weights are positive decimals between 0 and 100.").grid(row = 5 + (tickercount-1)*2, column = 1)
                    valid = False
                    break
        if valid is True:
            if sum(weights) != 100:
                Label(root, text = "Please make sure all weights add up to 100.").grid(row = 5 + (tickercount-1)*2, column = 1)
                valid = False
        if valid is True:
            
            entries = [(tickers[i], weights[i]) for i in range(len(tickers))]
            portfolios.addPortfolio(Portfolio(entries=entries, average=average, name=name))
            root.destroy()
            calculation_window()

def reset_main():
    root.destroy()
    main()

def createTickerSection(tickercount: int) -> None:
    if tickercount <= 0:
        Label(root, text = "Please make sure the number of tickers is a positive integer.").grid(row = 4, column = 1)
    else:
        for i in range(tickercount):
            ticker_section(startrow = 4 + 2*i)
        Button(root, text = "Reset Inputs (Existing strategies are preserved.)", command = reset_main).grid(row = 4 + (tickercount-1)*2, column = 0)
        Button(root, text = "Create Strategy", command = lambda: checkRequirements(tickercount)).grid(row = 5 + (tickercount-1)*2, column = 0)
        

def to_calculation_window():
    root.destroy()
    calculation_window()

def back_to_main(window: Tk):
    window.destroy()
    main()

def main():
    global root, name, sma
    root = Tk()
    root.title("GTAA Backtesting Tool by Lukas Florian Richter & Nemanja Cerovac")    
    Label(root, text = "Here you can backtest your GTAA strategies with custom securities and SMAs to use.").grid(row = 0, column = 0, columnspan=4)
    Button(root, text = "To calculation page", command = lambda: to_calculation_window()).grid(row = 2, column = 0)
    Button(root, text = "Quit", command = root.destroy).grid(row = 3, column = 0)
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
    global tickerlist, weightlist, portfolios
    tickerlist, weightlist, portfolios = [], [], Portfoliolist([])

    Button(root, text = "Enter Securities", command= lambda: createTickerSection(get_numberinput(tickerinput))).grid(row = 3, column = 3)
    #lambda because otherwise tkinter would run the command immediately after creating the button
    root.mainloop()

def calculation_window():
    app = Tk()
    app.title("Analyse your strategies")
    Button(app, text = "Back to strategy creation window", command = lambda: back_to_main(app)).grid(row = 0, column=0, columnspan=2)
    Label(text = "Select one strategy to create an analysis using the Buy and Hold strategy as a Benchmark.").grid(row = 1, column = 0, columnspan=2)
    Label(text = "Or select two portfolios to compare them.").grid(row = 2, column = 0, columnspan=2)
    optionlist = [name for name in portfolios.portfolios]
    default = StringVar(app, value = "No strategy chosen")
    default.set(optionlist[0])
    
    name1 = OptionMenu(app, variable=default, *optionlist)
    name1.grid(row = 3, column = )
    app.mainloop()
    

main()