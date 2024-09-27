import mysql.connector
import pandas as pd

# Database connection
def connect_to_database():
    connection = mysql.connector.connect(
        host="your_mysql_host",
        user="your_mysql_user",
        password="your_mysql_password",
        database="stock_data"
    )
    return connection

# Fetch data from MySQL
def get_data():
    conn = connect_to_database()
    query = "SELECT * FROM energy_consumption"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Example: Fetching the data and printing it
data = get_data()
print(data.head())

import streamlit as st
import pandas as pd

# MySQL connection function
def get_data():
    conn = mysql.connector.connect(
        host="your_mysql_host",
        user="your_mysql_user",
        password="your_mysql_password",
        database="stock_data"
    )
    query = "SELECT * FROM energy_consumption"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Streamlit app
def main():
    st.title("Energy Consumption Forecast")

    # Display data
    if st.button("Fetch Data"):
        data = get_data()
        st.write(data)

    # You can include more functionality like a file uploader, plots, etc.

if __name__ == "__main__":
    main()