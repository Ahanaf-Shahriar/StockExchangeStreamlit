import streamlit as st
from database import get_company_trading_data,get_holding_data
import pandas as pd 
import psycopg2
from postGreSQlconn import create_connection



company_trading_df = get_company_trading_data()

# Get the holding data
holding_data_df = get_holding_data()



def nav():
    # Create a sidebar
    st.sidebar.title("Dhaka Stock Exchange")
    
    # Add navigation links
    page = st.sidebar.radio("Go to", ("Overview", "Analysising info", "Performance Tracker","attrition"))
    
    # Render different pages based on the selected navigation link
    if page == "overview":
        st.header("OverView")
        # Add content for the home page
    elif page == "Demographics":
        st.header("Demographics")
        # Add content for the about page
    elif page == "Performance Tracker":
        st.header("Performance Tracker")
    elif page == "attrition":
        st.header("attrition")
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


# Run the Streamlit app
if __name__ == "__main__":
    search_database()