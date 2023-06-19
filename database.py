import psycopg2
import streamlit as st
import pandas as pd
from postGreSQlconn import create_connection


def get_company_trading_data():
    # Establish a connection to the PostgreSQL database
    conn = create_connection()
    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Execute a SELECT query to retrieve all records from the table
    cursor.execute("SELECT * FROM company_trading")

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]

    # Create a DataFrame from the fetched rows and column names
    company_trading_df = pd.DataFrame(rows, columns=columns)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return company_trading_df


def get_holding_data():
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
        host="localhost",  # Replace with your host address
        port="5432",  # Replace with your port number
        user="ahanafshahriar",  # Replace with your username
        database="holdingData"  # Replace with your database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Execute a SELECT query to retrieve all records from the table
    cursor.execute("SELECT * FROM holdingData")

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]

    # Create a DataFrame from the fetched rows and column names
    holding_data_df = pd.DataFrame(rows, columns=columns)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return holding_data_df

