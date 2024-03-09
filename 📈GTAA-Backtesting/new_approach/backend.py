import quantstats as qs

ticker = "eux.sg"
stock = qs.utils.download_return(ticker, period = "3y")
print(stock)