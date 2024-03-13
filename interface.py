import quantstats as qs
import datetime as dt
from classes import Portfoliolist, Portfolio
from tkinter import *
import yfinance as yf
import webbrowser
import os

def checkyFinance(ticker: str):
    try:
        name = yf.Ticker(ticker).info["longName"]
        return True
    except:
        return False

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
            if name.get() in portfolios.portfolios.keys() or name.get() == "None":
                Label(root, text = "Please make sure the strategy name is unique and is not \"None\".").grid(row = 5 + (tickercount-1)*2, column = 1)
                valid = False
        if valid is True:
            entries = [(tickers[i], weights[i]) for i in range(len(tickers))]
            portfolios.addPortfolio(Portfolio(entries=entries, average=average), name.get())
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
    tickerlist, weightlist = [], []

    Button(root, text = "Enter Securities", command= lambda: createTickerSection(get_numberinput(tickerinput))).grid(row = 3, column = 3)
    #lambda because otherwise tkinter would run the command immediately after creating the button
    root.mainloop()

def analyse(name1: Entry, name2: Entry) -> None:
    p1, p2 = name1.get(), name2.get()
    if p1 == "None" and p2 == "None":
        Label(text = "You have to select at least one strategy.").grid(row = 5, column= 0, columnspan=2)
    elif p1 == "None" and p2 != "None":
        Label(text = "Please be very patient, this may take a while.").grid(row = 5, column= 0, columnspan=2)
        gtaa, bh, first_date = portfolios.performCalulation(name = p2, start = dt.date(1900,1,1), end = dt.date.today())
        dir_path = os.path.dirname(os.path.realpath(__file__))
        qs.reports.html(returns=gtaa, benchmark=bh, title = p2 + " vs. Buy & Hold", output= p2 + "vsB&H.html")
        webbrowser.open("file://" + dir_path + "/" + p2 + "vsB&H.html")
    elif p1 != "None" and p2 == "None":
        Label(text = "Please be very patient, this may take a while.").grid(row = 5, column= 0, columnspan=2)
        gtaa, bh, first_date = portfolios.performCalulation(name = p1, start = dt.date(1900,1,1), end = dt.date.today())
        dir_path = os.path.dirname(os.path.realpath(__file__))
        qs.reports.html(returns=gtaa, benchmark=bh, title = p1 + " vs. Buy & Hold", output= p1 + "vsB&H.html")
        webbrowser.open("file://" + dir_path + "/" + p1 + "vsB&H.html")
    else:
        Label(text = "Please be very patient, this may take a while.").grid(row = 5, column= 0, columnspan=2)
        gtaa1, bh1, first_date1 = portfolios.performCalulation(name = p1, start = dt.date(1900,1,1), end = dt.date.today())
        gtaa2, bh2, first_date2 = portfolios.performCalulation(name = p2, start = dt.date(1900,1,1), end = dt.date.today())
        first_date = max(first_date1, first_date2)
        gtaa1, gtaa2 = gtaa1[first_date:], gtaa2[first_date:]
        dir_path = os.path.dirname(os.path.realpath(__file__))
        qs.reports.html(returns=gtaa1, benchmark=gtaa2, title = p1 + " vs. " + p2, output= p1 + "vs" + p2 + ".html")
        webbrowser.open("file://" + dir_path + "/" + p1 + "vs" + p2 + ".html")
        
    

def calculation_window():
    app = Tk()
    app.title("Analyse your strategies")
    Button(app, text = "Back to strategy creation window", command = lambda: back_to_main(app)).grid(row = 0, column=0, columnspan=2)
    Label(text = "Select one strategy to create an analysis using the Buy and Hold strategy as a Benchmark.").grid(row = 1, column = 0, columnspan=2)
    Label(text = "Or select two portfolios to compare them.").grid(row = 2, column = 0, columnspan=2)
    optionList = ["None"] + list(portfolios.portfolios.keys())
    variable1 = StringVar(app, value = None)
    variable1.set(optionList[0])
    variable2 = StringVar(app, value = None)
    variable2.set(optionList[0])
    name1 = OptionMenu(app, variable1, *optionList)
    name1.grid(row = 3, column = 0)
    name2 = OptionMenu(app, variable2, *optionList)
    name2.grid(row = 3, column = 1)
    Button(app, text = "Generate Analysis", command = lambda: analyse(variable1, variable2)).grid(row = 4, column = 0, columnspan=2)
    app.mainloop()

portfolios = Portfoliolist([])
main()