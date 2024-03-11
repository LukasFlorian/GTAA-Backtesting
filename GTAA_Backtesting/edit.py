import streamlit as st
from backend.classes import Portfolio, Entry
from backend.shared import *

st.title("📝 Edit an existing portfolio")

def change_name(portfolio: Portfolio, name: str):
    if name == "":
        st.error("Your portfolio cannot have an empty name")
    else:
        portfolio.set_name(new = name)
        st.success("Name changed successfully")

def change_sma(portfolio: Portfolio, new_sma: int):
    portfolio.set_average(new = new_sma)
    st.success("SMA changed successfully to " + str(portfolio.average))

def change_ticker(entry: Entry, newticker: str):
    if checkyFinance(newticker) is True:
        entry.set_ticker(newticker)
        st.success("Ticker changed successfully.")
    else:
        st.error("Make sure the ticker you enter is valid.")

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
                st.button(label = "Apply name change", key = str(tabindex) + "-" + str(2), on_click=change_name(portfolio, name))
            col1, col2 = st.columns([3,1])
            with col1:
                average = st.number_input(label = "Change the SMA", min_value = 7, max_value = 252, key = str(tabindex) + "-" + str(3))
            with col2:
                st.button(label = "Apply SMA change", key = str(tabindex) + "-" + str(4), on_click=change_sma(portfolio=portfolio, new_sma=average))
                    
            st.subheader("Positions:")
            entries = portfolio.entries
            for id in entries:
                entry = entries[id]
                st.write(entry.name)
                col1, col2= st.columns([3,1])
                with col1:
                    newticker = st.text_input(label="Change the ticker for this entry", value = entry.ticker, key = str(tabindex) + "-" + str(id) + "-" + str(1))
                with col2:
                    st.button(label="Change ticker", key = str(tabindex) + "-" + str(id) + "-" + str(2), on_click=change_ticker(entry, newticker))
            st.write("Feature to delete securities, adjust their weights or add new ones will be added in the future.")
            deletion = True
            st.button(label = "Delete Portfolio", key = str(tabindex) + "-" + str(7), on_click=portfolios.deletePortfolio(tabindex))

else:
    st.write("This page only becomes interesting when you've created your first portfolio.")