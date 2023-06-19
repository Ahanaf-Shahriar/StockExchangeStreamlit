import psycopg2


def create_connection():
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
        host="localhost",  # Replace with your host address
        port="5432",  # Replace with your port number
        user="ahanafshahriar",  # Replace with your username
        database="holdingData"  # Replace with your database name
    )
    
    return conn

# Get the company trading data

