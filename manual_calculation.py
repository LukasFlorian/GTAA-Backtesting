import quantstats as qs
import datetime as dt
from classes import Portfolio
import webbrowser
import os
from PIL import Image


p1 =Portfolio(entries = [("^GSPC", 50),
                         ("AAPL", 50)],
              average = 200)

p2 =Portfolio(entries = [("AAPL", 50)],
              average = 200)

start = dt.date(1900,1,1)
end = dt.date.today()


def gtaa_vs_bh(portfolio: Portfolio, strategyname: str) -> None:
    gtaa, bh, first_date = portfolio.relative_calculation(start = start, end = end)
    gtaa.name = strategyname
    dir_path = os.path.dirname(os.path.realpath(__file__))
    qs.reports.html(returns=gtaa, benchmark=bh, title = strategyname + " vs. Buy & Hold", output = dir_path + "/" + strategyname + "vsB&H.html")
    webbrowser.open("file://" + dir_path + "/" + strategyname + "vsB&H.html")

def gtaa1_vs_gtaa2(portfolio1: Portfolio, portfolio2: Portfolio, filename: str) -> None:
    gtaa1, bh1, first_date1 = portfolio1.relative_calculation(start = start, end = end)
    gtaa1.name = "GTAA1"
    gtaa2, bh2, first_date2 = portfolio2.relative_calculation(start = start, end = end)
    gtaa1.name = "GTAA2"
    first_date = max(first_date1, first_date2)
    gtaa1, gtaa2 = gtaa1[first_date:], gtaa2[first_date:]
    dir_path = os.path.dirname(os.path.realpath(__file__))
    qs.reports.html(returns=gtaa1, benchmark=gtaa2, title = filename, output = dir_path + "/" + filename + ".html")
    webbrowser.open("file://" + dir_path + "/" + filename + ".html")

#gtaa1_vs_gtaa2(p1, p2, "JustTesting")
gtaa_vs_bh(p1, "JustTesting")