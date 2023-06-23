import streamlit as st
from database import get_company_trading_data,get_holding_data
import pandas as pd 
import matplotlib.pyplot as plt

import psycopg2
from postGreSQlconn import create_connection
from Analysis import holding_trend_line_chart,sector_line_chart



company_trading_df = get_company_trading_data()

# Get the holding data
holding_data_df = get_holding_data()



def nav():
    # Create a sidebar
    st.sidebar.title("Dhaka Stock Exchange")
    
    # Add navigation links
    page = st.sidebar.radio("Go to", ("Overview", "Analysising info", "Holding info"))
    
    # Render different pages based on the selected navigation link
    if page == "overview":
        st.header("OverView")
        # Add content for the home page
    elif page == "Analysis info":
        st.header("Analysis info")
        # Add content for the about page
    elif page == "Holding info":
        st.header("Holding info")
    
        # Add content for the contact page

def search_data(query):
    # Establish a connection to the PostgreSQL database
    conn = create_connection()
    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Execute the search query
    cursor.execute(query)

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]

    # Create a DataFrame from the fetched rows and column names
    search_results_df = pd.DataFrame(rows, columns=columns)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return search_results_df


def company_data(): 
    number_of_companies = company_trading_df.shape[0]
    number_of_sector = company_trading_df['sector'].nunique()
    

    # Display the blocks side by side
    st.markdown(
        f"""
        <div style='display: flex;'>
            <div class='block green'>
                <h3>Number of Companies</h3>
                <p>{number_of_companies}</p>
            </div>
            <div class='block green'>
                <h3>sector</h3>
                <p>{number_of_sector}</p>
            </div>
           
          
        """,
        unsafe_allow_html=True
    )






# Define your Streamlit app
def search_database():
    # Title
    st.title("Database Search")

    # Select dataset
    dataset = st.selectbox("Select dataset", ("company_trading", "holding_data"))

    # Input search query
    search_query = st.text_input("Enter your search query:")

    # Search button
    if st.button("Search"):
        if dataset == "company_trading":
            # Perform the search in company_trading dataset
            results_df = search_data(f"SELECT * FROM company_trading WHERE Trading_code LIKE '%{search_query}%'")
        elif dataset == "holding_data":
            # Perform the search in holding_data dataset
            results_df = search_data(f"SELECT * FROM holdingData WHERE Company_ID LIKE '%{search_query}%'")
        else:
            st.write("Invalid dataset selected.")
            return

        # Display search results
        if len(results_df) > 0:
            st.write("Search Results:")
            st.dataframe(results_df)
        else:
            st.write("No results found.")



import streamlit as st
import plotly.graph_objects as go

def company_barchart(company_trading_df, holding_data_df):
    number_of_companies = holding_data_df.shape[0]
    sector_counts = company_trading_df['sector'].value_counts()

    # Create the bar chart
    data = [
        go.Bar(
            x=sector_counts.index,
            y=sector_counts.values,
            marker=dict(color='rgba(0, 195, 255, 0.325)')
        )
    ]

    # Set the layout
    layout = go.Layout(
        title='Number of Companies in Each Sector',
        xaxis=dict(title='Sector'),
        yaxis=dict(title='Number of Companies')
    )

    # Create the figure
    fig = go.Figure(data=data, layout=layout)

    # Display the names of the companies
   

    # Display the chart using Streamlit
    st.plotly_chart(fig)

# Example usage
# Assuming company_trading_df and holding_data_df are your DataFrames






# Run the Streamlit app
if __name__ == "__main__":
    company_trading_df = get_company_trading_data()

# Get the holding data
    holding_data_df = get_holding_data()
    css = open('style.css', 'r').read()

    # Link the CSS file
    st.markdown(f'<head><style>{css}</style></head>', unsafe_allow_html=True)
    nav()
    st.title("OverView")

    search_database()
    company_data()
    company_barchart(company_trading_df,holding_data_df)
    st.title("LINE CHART")
    holding_trend_line_chart(holding_data_df)
    st.title("Stock trend (Sectors)")
    sector_line_chart(holding_data_df , company_trading_df)
