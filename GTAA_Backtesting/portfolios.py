import streamlit as st
import pandas as pd
import datetime

# Updated data with additional entries
data = [
    [datetime.datetime(2024, 1, 1, 0, 0), 1.0],
    [datetime.datetime(2024, 1, 1, 0, 0), 1.0],
    [datetime.datetime(2024, 1, 1, 0, 0), 0.9936283306409684],
    [datetime.datetime(2024, 1, 1, 0, 0), 0.991152083345328],
    [datetime.datetime(2024, 1, 1, 0, 0), 0.9961598307582256],
    [datetime.datetime(2024, 1, 1, 0, 0), 0.9961598307582256],
    [datetime.datetime(2024, 1, 1, 0, 0), 0.9961598307582256],
    [datetime.datetime(2024, 1, 1, 0, 0), 1.0176452693213887],
    [datetime.datetime(2024, 1, 1, 0, 0), 1.0147380685916638],
    [datetime.datetime(2024, 1, 1, 0, 0), 1.0363942928090064],
    [datetime.datetime(2024, 1, 1, 0, 0), 1.0336231617749838],
    [datetime.datetime(2024, 1, 1, 0, 0), 1.0414714349397112],
    [datetime.datetime(2024, 1, 1, 0, 0), 1.0414714349397112],
    [datetime.datetime(2024, 1, 1, 0, 0), 1.0414714349397112],
    # Additional data
    [datetime.datetime(2024, 2, 1, 0, 0), 1.148273133624562],
    [datetime.datetime(2024, 2, 1, 0, 0), 1.145434679364536],
    [datetime.datetime(2024, 2, 1, 0, 0), 1.1755480429169445],
    [datetime.datetime(2024, 2, 1, 0, 0), 1.1674817215007973],
    [datetime.datetime(2024, 2, 1, 0, 0), 1.1674817215007973],
    [datetime.datetime(2024, 2, 1, 0, 0), 1.1674817215007973],
    [datetime.datetime(2024, 2, 1, 0, 0), 1.160550073239078],
    [datetime.datetime(2024, 2, 1, 0, 0), 1.17184801047552],
    [datetime.datetime(2024, 2, 1, 0, 0), 1.1643483593397055],
    [datetime.datetime(2024, 2, 1, 0, 0), 1.1706506756416402],
    [datetime.datetime(2024, 3, 1, 0, 0), 1.1706506756416402],
    [datetime.datetime(2024, 3, 1, 0, 0), 1.1706506756416402],
    [datetime.datetime(2024, 3, 1, 0, 0), 1.1706506756416402],
    [datetime.datetime(2024, 3, 1, 0, 0), 1.1658613492972139]
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
