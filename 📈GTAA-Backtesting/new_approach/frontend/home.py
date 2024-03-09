import streamlit as st
from st_pages import Page, show_pages

relative_prefix = "📈GTAA-Backtesting/new_approach/frontend/"
def add_prefix(filename: str) -> str:
    return relative_prefix + filename + ".py"
show_pages(
    [
        Page(add_prefix("home"), "Home", "🏠"),
        Page(add_prefix("new"), "New Allocation", "🆕"),
        Page(add_prefix("edit"), "Edit Allocation", "📝"),
        Page(add_prefix("portfolios"), "My Allocations", "📊"),
    ]
)

st.title("GTAA Backtesting Tool")
st.header("By Lukas Florian Richter & Nemanja Cerovac")


st.write("---")

st.subheader("🚀 Get started")

col1, col2 = st.columns([2,1])
with col1:
    st.write("To create your first allocation, click here:")    
    st.write("Here you can edit an existing allocation:")
    st.write("And here you analyze and compare your existing allocations:")
with col2:
    st.page_link(page = "new.py", label = ":blue[🆕 New Allocation]")    
    st.page_link(page = "edit.py", label = ":blue[📝 Edit Allocation]")
    st.page_link(page = "portfolios.py", label = ":blue[📊 My Allocations]")


st.subheader("❓ You want to know what GTAA is?")
st.write("Global Tactical Asset Allocation (GTAA) is an investment strategy powered by global macro and quantitative research. GTAA primarily invests across asset classes and geographies, leveraging diversification and sophisticated risk management to generate alpha even during volatile conditions.")
st.write("The rationale behind the Global Tactical Asset Allocation investment strategy is discretionary and driven by fundamentals, but it is backed extensively by quantitative research. The GTAA invests across global asset classes, such as stocks, bonds, currencies, and commodities. The primary objective of global tactical asset allocation is to deliver alpha via asset allocation and diversification instead of just individual security selection.")
st.write("GTAA investment strategy is flexible across several dimensions and allows managers to dynamically shift the portfolio across various asset classes and instruments. This tactical allocation aims to deliver enticing risk-adjusted returns and simultaneously manage risk and control drawdowns.")
st.write("Most Global Tactical Asset Allocation funds adopt various strategies ranging from global macro to thematic and multi-asset investing for portfolio management. They focus on significant macroeconomic and structural transformations that lead to inefficiencies and risk/ reward opportunities.")

def link(description: str, url: str) -> None:
    col1, col2 = st.columns([len(description), len(url)])
    with col1:
        st.write(description)
    with col2:
        st.page_link(page = url, label = ":blue[" + url + "]")
link("Source:", "https://analyzingalpha.com/global-tactical-asset-allocation")

st.write("You can find additional information on the GTAA strategy here:")
link("Meb Faber's paper on the GTAA strategy:", "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=962461")

st.write("The Dual Momentum strategy is closely related to the momentum-based GTAA strategy:")
link("Gary Antonacci's paper on the Dual Momentum strategy:", "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2042750")