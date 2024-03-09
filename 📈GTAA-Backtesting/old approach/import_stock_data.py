import yfinance as yf
import datetime as dt
from dateutil import relativedelta
import pandas as pd


def openConnection() -> tuple:
    """used to open database connection, informs about status of connection (successful or not)

    Returns:
        cur, conn: cursor for and connection to database
    """
    database = "/workspaces/Laufzeitoptimierung/📈GTAA-Backtesting/data/gtaa_database.db"
    try:
        conn = sql.connect(database)
        print("Database Sqlite3.db formed.") 
    except:
        raise Exception("Database Sqlite3.db not formed.")
        #print("Database Sqlite3.db not formed.")
        
    cur = conn.cursor()
    return cur, conn

def initialize() -> None:
    """initial creation of database with stocks table for stock ticker and name and historic table with historic prices for stocks on any given date
    """
    cur, conn = openConnection()
    cur.execute("CREATE TABLE Stocks (ticker TEXT PRIMARY KEY, name TEXT NOT NULL)")
    cur.execute("CREATE TABLE Historic (ticker TEXT NOT NULL, date TEXT NOT NULL, quote INT NOT NULL, ttm_sma INT NOT NULL, two_day_sma INT NOT NULL, ten_month_sma INT NOT NULL, six_month_sma INT NOT NULL, five_month_sma INT NOT NULL, three_month_sma INT NOT NULL, two_month_sma INT NOT NULL, PRIMARY KEY (ticker, date), FOREIGN KEY (ticker) REFERENCES Stocks(ticker))")
    conn.close()

def dropAll() -> None:
    """used to delete all database tables in case it needs to be re-initialized
    """
    cur, conn = openConnection()
    cur.execute("DROP TABLE Stocks")
    cur.execute("DROP TABLE Historic")
    conn.close()

#dropAll()
#initialize()

def getAverages(ttm: list, last_200: list, last_10m: list, last_6m: list, last_5m: list, last_3m: list, last_2m: list, quote: float, quote_date: dt.datetime):
    """calculates the averages for a stock

    Args:
        ttm (_type_): trailing twelve months
        last_200 (_type_): last 200 trading days (about a year)
        last_10m (_type_): last 10 months
        last_6m (_type_): last 6 months
        last_5m (_type_): last 5 months
        last_3m (_type_): last 3 months
        last_2m (_type_): last 2 months
        quote (_type_): quote on quote_date
        quote_date (_type_): date of quote
    """
    
    cur, conn = openConnection()
    def getTtm(avList: list) -> list:
        """average over trailing twelve months

        Args:
            avList (list): list of lists with format [date, quote on date, ttm average on date] 
        """
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
        return avList
    
    
    def get200d(avList: list) -> list:
        """average over last 200 trading days

        Args:
            avList (list): list of lists with format [date, quote on date, 200d average on date] of 200d averages in database 
        """
        #print(avList)
        avList.append([quote_date, quote])
        if len(avList) == 1:
            avList[0] = avList[0] + [None]
        else:
            lendif = max(len(avList) - 201, 1) #current day irrelevant
            avList = avList[lendif:]
            print(lendif, len(avList))
            sum = 0
            for entry in avList:
                sum += entry[1]
            average = sum/len(avList)
            avList[-1] = [avList[-1][0], avList[-1][1], average]
        return avList
    
    def get_x_m(avList: list, num_months: int) -> list:
        #print(avList, num_months)
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
        return avList
    
    ttm = getTtm(ttm)
    last_200 = get200d(last_200)
    last_10m = get_x_m(last_10m, 10)
    last_6m = get_x_m(last_6m, 6)
    last_5m = get_x_m(last_5m, 5)
    last_3m = get_x_m(last_3m, 3)
    last_2m = get_x_m(last_2m, 2)
    
    
    conn.close()
    return ttm, last_200, last_10m, last_6m, last_5m, last_3m, last_2m


def addStockData(ticker: str) -> None:
    """ importing new stocks not yet in the database
    
    Args:
        ticker (str): ticker whose stock info should be added
    """
    cur, conn = openConnection()
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
    conn.close()

def updateStockData(ticker: str) -> None:
    cur, conn = openConnection()
    """
    used to update data for listed stock with ticker
    """
    def averageSince(avList, num_months, last, price):
        """_summary_
        Args:
            avList (_type_): list of averages for the past num_months months
            num_months (_type_): number of months the avList is for
            last (_type_): last (most recent) date in avList
            price (_type_): price on a given day
        """
        print(avList)
        latest = []
        earliest = dt.datetime.now() - relativedelta.relativedelta(months = months)
        avList = avList[::-1]
        #find first valid date that should be included in the new avList
        first_valid = 0
        while (avList[first_valid][0] - last_date)/dt.timedelta(days = 1) < 0:
            first_valid += 1
        avList = avList[first_valid:]
        trading_days = len(avList)
        indices = [12, 200, 10, 6, 5, 3, 2]
        index = indices.index(num_months) + 3
        avList = avList[first_valid]

        #new

    cur.execute("SELECT date, quote FROM Historic WHERE Historic.ticker = \'" + ticker + "\' ORDER BY date desc")
    data = cur.fetchall()
    #print(data[0])
    latest = data[0][0]
    if (dt.datetime.now()-dt.datetime.strptime(latest, '%Y-%m-%d'))/dt.timedelta(days = 1) > 0:
        pass
    #print(type(latest))
    conn.close()
    
dropAll()
initialize()
addStockData("META")
updateStockData("META")