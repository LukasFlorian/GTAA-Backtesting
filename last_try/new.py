import streamlit as st
from backend.classes import Portfolio
import quantstats as qs
import yfinance as yf
import pandas as pd
import datetime as dt

st.title("🆕 Create a new calculation")

def add_row():
    if 'rows' not in st.session_state:
        st.session_state.rows = [{'ticker': '', 'weight': 0.0}]
    else:
        st.session_state.rows.append({'ticker': '', 'weight': 0.0})

def remove_row(index):
    if 'rows' in st.session_state and len(st.session_state.rows) > 0:
        st.session_state.rows.pop(index)

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

name = st.text_input(label = "What should your portfolio be called?")
average = st.number_input(label = "How many trading days should the SMA include?", min_value=7, max_value=252)
st.subheader("Positions:")
if 'rows' not in st.session_state:
    add_row()

for index, row in enumerate(st.session_state.rows):
    cols = st.columns([3, 3, 1])
    with cols[0]:
        st.session_state.rows[index]['ticker'] = st.text_input("Ticker Symbol", value=row['ticker'], key=f"ticker_{index}")
    with cols[1]:
        st.session_state.rows[index]['weight'] = st.number_input("Weight in %", value=1.0, min_value=0.01, max_value=100.0, format="%f", key=f"weight_{index}")
    with cols[2]:
        st.button("Remove Row", on_click=lambda index=index: remove_row(index), key=f"remove_{index}")

st.button("Add Row", on_click=add_row)
first_portfolio = False
# Automatic total weight check after each change
total_weight = sum(row['weight'] for row in st.session_state.rows)
if total_weight == 100:
    if st.button("Create Portfolio"):
        allTickers = True
        for row in st.session_state.rows:
            allTickers = bool(checkyFinance(ticker=row["ticker"]) == allTickers)
        if allTickers == True and name != "":
            portfolio_list = [(row['ticker'], row['weight']) for row in st.session_state.rows]
            if first_portfolio == False:
                portfolio1 = Portfolio(entries = portfolio_list, average = average, name = name)
            else:
                portfolio2 = Portfolio(entries = portfolio_list, average = average, name = name)
            st.success("Portfolio created.")
            first_portfolio = True
        else:
            st.error("Portfolio not created. Please make sure the portfolio name is not empty and that all tickers are valid and exist on yahooFinance.")
elif total_weight < 100:
    st.error(f"Total weight is less than 100% ({total_weight}%)")
else:
    st.error(f"Total weight exceeds 100% ({total_weight}%)")

if first_portfolio == True:
    st.write("Now that you created your first portfolio, you have four options:")
    st.write("1. By clicking \"Spreadsheet without benchmark\", I will generate a spreadsheet to analyse your portfolio without a benchmark.")
    st.write("2. By clicking \"Spreadsheet with B&H\", I will generate a spreadsheet to analyse your portfolio in comparison to the Buy- and Hold-Strategy with the same securities.")
    st.write("3. By clicking \"Spreadsheet with second portfolio\", I will create a second portfolio from the above securities and generate a spreadsheet to compare the two GTAA strategies.")
    st.write("4. If you click on \"Dismiss\", I will dismiss all your portfolios so you can create new ones.")
    if st.button("Spreadsheet without benchmark"):
        st.write("1")
        earliest = portfolio1.get_earliest()
        print(earliest)
        if earliest == None:
            st.error("Please reset your portfolio and choose a smaller number of days for the SMA or different securities as there is not enough data available.")
        else:
            start = st.date_input(label = "Please choose the start date for your calculation", min_value=earliest, max_value=dt.datetime.now())
            end = st.date_input(label = "Please choose the end date for your calculation", min_value=start, max_value=dt.datetime.now())
            if st.button(label = "Calculate"):
                gtaa = portfolio1.gtaa_relative_calculation(start=start, end=end)
                gtaa_dict = {entry[0]: entry[1] for entry in gtaa}
                gtaa_dataframe = pd.DataFrame.from_dict(gtaa_dict, columns = ["Value"], orient = "index").rename_axis("Date")
                qs.reports.html(gtaa_dataframe, output = "report.html")