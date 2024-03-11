import streamlit as st

st.title("🆕 Create a New Portfolio")

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
    # Join each tuple into a string and then join all strings into one to display
    portfolio_list_str = ', '.join([f"('{ticker}', {weight})" for ticker, weight in portfolio_list])
    st.text(f"[{portfolio_list_str}]")


if 'rows' not in st.session_state:
    add_row()

for index, row in enumerate(st.session_state.rows):
    cols = st.columns([3, 3, 1])
    with cols[0]:
        st.session_state.rows[index]['ticker'] = st.text_input(f"Ticker Symbol Row {index+1}", value=row['ticker'], key=f"ticker_{index}")
    with cols[1]:
        st.session_state.rows[index]['weight'] = st.number_input(f"Weight in % Row {index+1}", value=row['weight'], min_value=0.0, max_value=100.0, format="%f", key=f"weight_{index}")
    with cols[2]:
        st.button("Remove Row", on_click=lambda index=index: remove_row(index), key=f"remove_{index}")

st.button("Add Row", on_click=add_row)

# Automatic total weight check after each change
total_weight = sum(row['weight'] for row in st.session_state.rows)
if total_weight == 100:
    st.success("Total weight is exactly 100%")
    # Display the button for creating a portfolio list when the total weight is exactly 100%
    if st.button("Create Portfolio List"):
        create_portfolio_list()
elif total_weight < 100:
    st.warning(f"Total weight is less than 100% ({total_weight}%)")
else:
    st.error(f"Total weight exceeds 100% ({total_weight}%)")
