import streamlit as st
from backend.classes import Portfolio
from backend.shared import *

st.title("📝 Edit an existing portfolio")

def add_row():
    if 'rows' not in st.session_state:
        st.session_state.rows = [{'ticker': '', 'weight': 0.0}]
    else:
        st.session_state.rows.append({'ticker': '', 'weight': 0.0})

def remove_row(index):
    if 'rows' in st.session_state and len(st.session_state.rows) > 0:
        st.session_state.rows.pop(index)

def create_portfolio_list():
    portfolio_list = [(row['ticker'], row['weight']) for row in st.session_state.rows]
    portfolios.addPortfolio(portfolio = Portfolio(entries = portfolio_list, average = average, name = name))

if len(portfolios.portfolios) > 0:
    tablist = [portfolios.portfolios[key].name for key in portfolios.portfolios]
    tabs = st.tabs(tablist)
    tabindex = -1
    for tab in tabs:
        tabindex += 1
        with tab:
            portfolio = portfolios.portfolios[tabindex]
            st.header(portfolio.name)
            col1, col2 = st.columns([3,1])
            with col1:
                name = st.text_input(label = "Change your portfolio name", key = str(tabindex) + "-" + str(1))
            with col2:
                if st.button(label = "Apply name change", key = str(tabindex) + "-" + str(2)):
                    if name != "":
                        portfolio.set_name(name)
                        st.success("Name changed successfully")
                    else:
                        st.error("Your portfolio cannot have an empty name")
            col1, col2 = st.columns([3,1])
            with col1:
                average = st.number_input(label = "Change the SMA", min_value = 7, max_value = 252, key = str(tabindex) + "-" + str(3))
            with col2:
                if st.button(label = "Apply SMA change", key = str(tabindex) + "-" + str(4)):
                    portfolio.set_average(average)
                    
            st.subheader("Positions:")
            entries = portfolio.entries
            for id in entries:
                entry = entries[id]
                st.write(entry.name)
                col1, col2= st.columns([3,1])
                with col1:
                    newticker = st.text_input(label="Change the ticker for this entry", value = entry.ticker, key = str(tabindex) + "-" + str(5))
                with col2:
                    if st.button(label="Change ticker", key = str(tabindex) + "-" + str(6)):
                        if checkyFinance(newticker) is True:
                            entry.set_ticker(newticker)
                            st.success("Ticker changed successfully.")
                        else:
                            st.error("Make sure the ticker you enter is valid.")
            st.write("Feature to delete securities, adjust their weights or add new ones will be added in the future.")
            deletion = True
            if st.button(label = "Delete Portfolio", key = str(tabindex) + "-" + str(7)) and deletion is True:
                st.write("Are you sure you want to delete this portfolio?", key = str(tabindex) + "-" + str(8))
                if st.button(label = "Yes"):
                    portfolios.deletePortfolio(tabindex)
                elif st.button(label = "No", key = str(tabindex) + "-" + str(9)):
                    deletion = False

else:
    st.write("This page only becomes interesting when you've created your first portfolio.")