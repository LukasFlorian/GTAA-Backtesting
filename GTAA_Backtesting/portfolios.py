import shared
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

portfolios = shared.Portfoliolist.portfolios

# Function to generate pie chart for portfolio composition
def plot_pie_chart(portfolio):
    weights = portfolio.weights  # Dictionary of weights
    stock_names = [portfolio.entries[i].name for i in portfolio.entries]  # List of stock names
    sizes = [weights[i] for i in weights]  # List of weights corresponding to stock names

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=stock_names, autopct='%1.1f%%')
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    return fig

# Function to generate performance diagram
def plot_performance_diagram(portfolio):
    start = dt.datetime(year=2024, month=1, day=1)
    end = dt.datetime.now()
    performance_data = portfolio.gtaa_relative_calculation(start, end)

    # Example performance data structure (adjust according to your actual data structure)
    # performance_data = {'dates': [date_list], 'values': [value_list]}

    fig, ax = plt.subplots()
    ax.plot(performance_data['dates'], performance_data['values'])
    ax.set_title("Portfolio Performance Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Performance")
    return fig

# Streamlit UI
st.title('Portfolios Page')

# Dropdown to select a portfolio
selected_portfolio_name = st.selectbox('Select a Portfolio', [portfolio.name for portfolio in portfolios])
selected_portfolio = next((portfolio for portfolio in portfolios if portfolio.name == selected_portfolio_name), None)

if selected_portfolio:
    # Plotting the pie chart for the selected portfolio
    pie_chart_fig = plot_pie_chart(selected_portfolio)
    st.pyplot(pie_chart_fig)

    # Plotting the performance diagram for the selected portfolio
    performance_fig = plot_performance_diagram(selected_portfolio)
    st.pyplot(performance_fig)


'''
data = [
    [datetime.datetime(2024, 1, 1, 0, 0), 1.0],
    [datetime.datetime(2024, 1, 2, 0, 0), 1.0],
    [datetime.datetime(2024, 1, 3, 0, 0), 0.9928368680654219],
    [datetime.datetime(2024, 1, 4, 0, 0), 0.9914677145673791],
    [datetime.datetime(2024, 1, 5, 0, 0), 0.9920507870324119],
    [datetime.datetime(2024, 1, 6, 0, 0), 0.9920507870324119],
    [datetime.datetime(2024, 1, 7, 0, 0), 0.9920507870324119],
    [datetime.datetime(2024, 1, 8, 0, 0), 1.0014084977637705],
    [datetime.datetime(2024, 1, 9, 0, 0), 0.9986440316679214],
    [datetime.datetime(2024, 1, 10, 0, 0), 0.9996909274546752],
    [datetime.datetime(2024, 1, 11, 0, 0), 1.0015252646334296],
    [datetime.datetime(2024, 1, 12, 0, 0), 1.0037163433923717],
    [datetime.datetime(2024, 1, 13, 0, 0), 1.0037163433923717],
    [datetime.datetime(2024, 1, 14, 0, 0), 1.0037163433923717],
    [datetime.datetime(2024, 1, 15, 0, 0), 1.0037163433923717],
    [datetime.datetime(2024, 1, 16, 0, 0), 0.9941571828794109],
    [datetime.datetime(2024, 1, 17, 0, 0), 0.9844743960079851],
    [datetime.datetime(2024, 1, 18, 0, 0), 0.9854238813717681],
    [datetime.datetime(2024, 1, 19, 0, 0), 0.9903366492426007],
    [datetime.datetime(2024, 1, 20, 0, 0), 0.9903366492426007],
    [datetime.datetime(2024, 1, 21, 0, 0), 0.9903366492426007],
    [datetime.datetime(2024, 1, 22, 0, 0), 0.9880514759645608],
    [datetime.datetime(2024, 1, 23, 0, 0), 0.9897509995047188],
    [datetime.datetime(2024, 1, 24, 0, 0), 0.9858182647954519],
    [datetime.datetime(2024, 1, 25, 0, 0), 0.9905601263532156],
    [datetime.datetime(2024, 1, 26, 0, 0), 0.9892844067467212],
    [datetime.datetime(2024, 1, 27, 0, 0), 0.9892844067467212],
    [datetime.datetime(2024, 1, 28, 0, 0), 0.9892844067467212],
    [datetime.datetime(2024, 1, 29, 0, 0), 0.9944246217422155],
    [datetime.datetime(2024, 1, 30, 0, 0), 0.9954626251305261],
    [datetime.datetime(2024, 1, 31, 0, 0), 0.9899194788066162],
    [datetime.datetime(2024, 2, 1, 0, 0), 0.9899194788066162],
    [datetime.datetime(2024, 2, 2, 0, 0), 0.9860185053060381],
    [datetime.datetime(2024, 2, 3, 0, 0), 0.9860185053060381],
    [datetime.datetime(2024, 2, 4, 0, 0), 0.9860185053060381],
    [datetime.datetime(2024, 2, 5, 0, 0), 0.9813523715091845],
    [datetime.datetime(2024, 2, 6, 0, 0), 0.9850773485880683],
    [datetime.datetime(2024, 2, 7, 0, 0), 0.9862208376779251],
    [datetime.datetime(2024, 2, 8, 0, 0), 0.9851854195513752],
    [datetime.datetime(2024, 2, 9, 0, 0), 0.9859164472992161],
    [datetime.datetime(2024, 2, 10, 0, 0), 0.9859164472992161],
    [datetime.datetime(2024, 2, 11, 0, 0), 0.9859164472992161],
    [datetime.datetime(2024, 2, 12, 0, 0), 0.9857382752776827],
    [datetime.datetime(2024, 2, 13, 0, 0), 0.9751260458609283],
    [datetime.datetime(2024, 2, 14, 0, 0), 0.9798115033483623],
    [datetime.datetime(2024, 2, 15, 0, 0), 0.9850287956643227],
    [datetime.datetime(2024, 2, 16, 0, 0), 0.9842361223360471],
    [datetime.datetime(2024, 2, 17, 0, 0), 0.9842361223360471],
    [datetime.datetime(2024, 2, 18, 0, 0), 0.9842361223360471],
    [datetime.datetime(2024, 2, 19, 0, 0), 0.9842361223360471],
    [datetime.datetime(2024, 2, 20, 0, 0), 0.9853354453063311],
    [datetime.datetime(2024, 2, 21, 0, 0), 0.985143031504932],
    [datetime.datetime(2024, 2, 22, 0, 0), 0.9917408481830818],
    [datetime.datetime(2024, 2, 23, 0, 0), 0.9940550899580747],
    [datetime.datetime(2024, 2, 24, 0, 0), 0.9940550899580747],
    [datetime.datetime(2024, 2, 25, 0, 0), 0.9940550899580747],
    [datetime.datetime(2024, 2, 26, 0, 0), 0.9922669822825605],
    [datetime.datetime(2024, 2, 27, 0, 0), 0.9925275510279112],
    [datetime.datetime(2024, 2, 28, 0, 0), 0.9920603878000736],
    [datetime.datetime(2024, 2, 29, 0, 0), 0.9950500158989313],
    [datetime.datetime(2024, 3, 1, 0, 0), 0.9950500158989313],
    [datetime.datetime(2024, 3, 2, 0, 0), 0.9950500158989313],
    [datetime.datetime(2024, 3, 3, 0, 0), 0.9950500158989313],
    [datetime.datetime(2024, 3, 4, 0, 0), 0.9975212566959827],
    [datetime.datetime(2024, 3, 5, 0, 0), 0.9963553995036385],
    [datetime.datetime(2024, 3, 6, 0, 0), 1.001385580211321],
    [datetime.datetime(2024, 3, 7, 0, 0), 1.0069619730629282],
    [datetime.datetime(2024, 3, 8, 0, 0), 1.006737854051921],
    [datetime.datetime(2024, 3, 9, 0, 0), 1.006737854051921],
    [datetime.datetime(2024, 3, 10, 0, 0), 1.006737854051921],
    [datetime.datetime(2024, 3, 11, 0, 0), 1.006737854051921],

]

# Convert your data into a DataFrame
df = pd.DataFrame(data, columns=['Date', 'Value'])

# Create a Streamlit application
def main():
    st.title('Data Visualization')

    # Plotting the chart
    st.line_chart(df.set_index('Date'))

if __name__ == '__main__':
    main()
'''
