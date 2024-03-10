import streamlit as st

st.title("🆕 Create a New Portfolio")


def add_row():

    if 'rows' not in st.session_state:
        st.session_state.rows = [{'int': 0, 'float': 0.0}]
    else:
        st.session_state.rows.append({'int': 0, 'float': 0.0})

def remove_row():
    if 'rows' in st.session_state and len(st.session_state.rows) > 1:
        st.session_state.rows.pop()

if 'rows' not in st.session_state:
    add_row()


for index, row in enumerate(st.session_state.rows):
    cols = st.columns([3, 3, 1])  
    with cols[0]:
        st.session_state.rows[index]['int'] = st.number_input(f"Integer Value Row {index+1}", value=row['int'], format="%d", key=f"int_{index}")
    with cols[1]:
        st.session_state.rows[index]['float'] = st.number_input(f"Float Value Row {index+1}", value=row['float'], format="%f", key=f"float_{index}")
    with cols[2]:
        st.button("Remove Row", on_click=remove_row)




st.button("Add Row", on_click=add_row)

if st.button("Check if Total Floats = 100"):
    total_float = sum(row['float'] for row in st.session_state.rows)
    if total_float == 100:
        st.success("passt")
    else:
        st.error(f"float nicht genau 100")