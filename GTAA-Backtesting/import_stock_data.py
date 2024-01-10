import yfinance as yf
import sqlite3 as sql
import datetime as dt
from dateutil import relativedelta
import pandas as pd

database = "/Users/lukas/Library/Mobile Documents/com~apple~CloudDocs/Random_Coding/own_projects/gtaa_backtesting/data/gtaa_database.db"
try:
    conn = sql.connect(database)
    print("Database Sqlite3.db formed.") 
except:
    print("Database Sqlite3.db not formed.")
    
cur = conn.cursor()

def initialize():
    cur.execute("CREATE TABLE Stocks (ticker TEXT PRIMARY KEY, name TEXT NOT NULL)")
    cur.execute("CREATE TABLE Historic (ticker TEXT NOT NULL, date TEXT NOT NULL, quote INT NOT NULL, ttm_sma INT NOT NULL, two_day_sma INT NOT NULL, ten_month_sma INT NOT NULL, six_month_sma INT NOT NULL, five_month_sma INT NOT NULL, three_month_sma INT NOT NULL, two_month_sma INT NOT NULL, PRIMARY KEY (ticker, date), FOREIGN KEY (ticker) REFERENCES Stocks(ticker))")

def dropAll():
    cur.execute("DROP TABLE Stocks")
    cur.execute("DROP TABLE Historic")

dropAll()
initialize()

def getAverages(ttm, last_200, last_10m, last_6m, last_5m, last_3m, last_2m, quote, quote_date):
    def getTtm(avList):
        last_date = quote_date - relativedelta.relativedelta(years = 1)
        avList.append([quote_date, quote])
        first_valid = 0
        while (avList[first_valid][0] - last_date)/dt.timedelta(days = 1) < 0:
            first_valid += 1
        avList = avList[first_valid:]
        sum = 0
        for entry in avList:
            sum += entry[1]
        average = sum/len(avList)
        avList[-1] = [avList[-1][0], avList[-1][1], average]
        return(avList)
    
    def get200d(avList):
        avList.append([quote_date, quote])
        lendif = len(avList) - 201 #current day irrelevant
        avList = avList[lendif:]
        sum = 0
        for entry in avList:
            sum += entry[1]
        average = sum/len(avList)
        avList[-1] = [avList[-1][0], avList[-1][1], average]
        return(avList)
    
    def get_x_m(avList, num_months):
        last_date = quote_date - relativedelta.relativedelta(months = num_months)
        avList.append([quote_date, quote])
        first_valid = 0
        while (avList[first_valid][0] - last_date)/dt.timedelta(days = 1) < 0:
            first_valid += 1
        avList = avList[first_valid:]
        sum = 0
        for entry in avList:
            sum += entry[1]
        average = sum/len(avList)
        avList[-1] = [avList[-1][0], avList[-1][1], average]
        return(avList)
    
    ttm = getTtm(ttm)
    last_200 = get200d(last_200)
    last_10m = get_x_m(last_10m, 10)
    last_6m = get_x_m(last_6m, 6)
    last_5m = get_x_m(last_5m, 5)
    last_3m = get_x_m(last_3m, 3)
    last_2m = get_x_m(last_2m, 2)
    return(ttm, last_200, last_10m, last_6m, last_5m, last_3m, last_2m)


def addStockData(ticker):
    stock_info = yf.Ticker(ticker)
    
    name = stock_info.info["longName"]
    cur.execute("INSERT INTO Stocks VALUES (\'" + ticker + "\', \'" + name + "\')")
    
    historic_data = stock_info.history(period = "max")
    dates = historic_data.index.values
    close_quotes = historic_data['Close']

    ttm = []
    last_200 = []
    last_10m = []
    last_6m = []
    last_5m = []
    last_3m = []
    last_2m = []
    for index in range(len(dates)):
        date = str(dates[index])[:10]
        quote = float(close_quotes.iloc[index])
        quote_date = dt.datetime.strptime(date, '%Y-%m-%d')
        ttm, last_200, last_10m, last_6m, last_5m, last_3m, last_2m = getAverages(ttm, last_200, last_10m, last_6m, last_5m, last_3m, last_2m, quote, quote_date)
        cur.execute("INSERT INTO Historic VALUES (\'" + ticker + "\', \'" + date + "\', \'" + str(quote) + "\', \'" + str(ttm[-1][2]) + "\', \'" + str(last_200[-1][2]) + "\', \'" + str(last_10m[-1][2]) + "\', \'" + str(last_6m[-1][2]) + "\', \'" + str(last_5m[-1][2]) + "\', \'" + str(last_3m[-1][2]) + "\', \'" + str(last_2m[-1][2]) + "\')")
    conn.commit()

def updateStockData(ticker):
    cur.execute("SELECT date, quote FROM Historic WHERE Historic.ticker = \'" + ticker + "\' ORDER BY date desc")
    latest = cur.fetchall()
    
    print(str(latest))
    
    
addStockData("META")
updateStockData("META")


conn.close()