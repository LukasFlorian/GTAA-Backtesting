import streamlit as st
from backend.classes import Portfolio
from backend.shared import *

st.title("🆕 Create a New Portfolio")

def add_row():
    if 'rows' not in st.session_state:
        st.session_state.rows = [{'ticker': '', 'weight': 0.0}]
    else:
        st.session_state.rows.append({'ticker': '', 'weight': 0.0})

def remove_row(index):
    if 'rows' in st.session_state and len(st.session_state.rows) > 0:
        st.session_state.rows.pop(index)


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

# Automatic total weight check after each change
total_weight = sum(row['weight'] for row in st.session_state.rows)
if total_weight == 100:
    if st.button("Create Portfolio"):
        allTickers = True
        for row in st.session_state.rows:
            allTickers = bool(checkyFinance(ticker=row["ticker"]) == allTickers)
        if allTickers == True and name != "":
            portfolio_list = [(row['ticker'], row['weight']) for row in st.session_state.rows]
            portfolios.addPortfolio(portfolio = Portfolio(entries = portfolio_list, average = average, name = name))
            print(portfolios.num_portfolios)
            st.success("Portfolio created.")
            st.write("Create another portfolio or head to the \"📊 My Allocations\" section in the sidebar to look at the data for your portfolio.")
        else:
            st.error("Portfolio not created. Please make sure the portfolio name is not empty and that all tickers are valid and exist on yahooFinance.")
elif total_weight < 100:
    st.error(f"Total weight is less than 100% ({total_weight}%)")
else:
    st.error(f"Total weight exceeds 100% ({total_weight}%)")
