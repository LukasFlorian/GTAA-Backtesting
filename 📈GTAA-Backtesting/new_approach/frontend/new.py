import streamlit as st

st.title("🆕 Create a new portfolio")

numberPositions = int(st.number_input(label = "Number of Positions", help = "The number of positions your portfolio should have", format = "%d", step = 1, value = 1))