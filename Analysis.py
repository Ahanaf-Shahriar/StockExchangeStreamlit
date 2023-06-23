import streamlit as st
from database import get_company_trading_data,get_holding_data
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np


def holding_trend_line_chart(holding_data):

    # Extract unique company names
    company_names = holding_data["company_id"].unique()

    # Allow user to select one or more company names
    selected_companies = st.multiselect("Select Company(s)", company_names)

    # Filter the DataFrame based on selected company names
    filtered_data = holding_data[holding_data["company_id"].isin(selected_companies)]

    # Create separate line charts for each selected company
    for company in selected_companies:
        # Extract data for the current company
        company_data = filtered_data[filtered_data["company_id"] == company]

        # Extract the desired columns for the line chart
        chart_data = company_data[["date", "sponsor", "govt", "institute", "Foreign", "public"]]

        # Convert the "Date" column to datetime
        chart_data["date"] = pd.to_datetime(chart_data["date"])

        # Set the "Date" column as the index
        chart_data.set_index("date", inplace=True)

        # Generate the line chart for the current company
        st.line_chart(chart_data)


def sector_line_chart(holding_data , trading_data): 

    new_df = pd.DataFrame({
    'companyname': trading_data['companyname'],
    'trading_code': trading_data['trading_code'],
    'sector': trading_data['sector'],
    'company_id': holding_data['company_id'],
    'date': holding_data['date'],
    'sponsor': holding_data['sponsor'],
    'govt': holding_data['govt']
})
    st.write(new_df)

