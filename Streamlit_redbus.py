import streamlit as st
import pymysql
import pandas as pd

# Function to connect to the MySQL database
def get_connection():
    return  pymysql.connect(host="localhost", 
    user="root", 
    passwd="Iyyappan1*", 
    database="redbus"  # Database name
    )
# Function to fetch unique Route_Name values
def fetch_unique_route_names():
    query = "SELECT DISTINCT Route_Name FROM bus_routes ORDER BY Route_Name"
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df['Route_Name'].tolist()

# Function to fetch data from the database
def fetch_bus_routes(route_name=None):
    query = "SELECT * FROM bus_routes"
    params = ()

    if route_name:
        query += " WHERE Route_Name = %s"
        params = (route_name,)

    conn = get_connection()
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

# Streamlit app interface
st.title("RedBus Routes Viewer")
st.write("This app interacts with the RedBus database to fetch and display bus routes.")

# Fetch unique Route_Names for the dropdown
unique_route_names = fetch_unique_route_names()

# Dropdown for selecting Route_Name
selected_route_name = st.selectbox("Select a Route Name:", options=["All Routes"] + unique_route_names)

# Fetch data based on the selected route name
if selected_route_name == "All Routes":
    data = fetch_bus_routes()  # Fetch all data
else:
    data = fetch_bus_routes(selected_route_name)  # Fetch data for the selected route

# Display data in a table
if not data.empty:
    st.dataframe(data)
else:
    st.write("No routes found for the selected filter.")

# Option to download data
csv = data.to_csv(index=False)
st.download_button(
    label="Download Data as CSV",
    data=csv,
    file_name="bus_routes.csv",
    mime="text/csv"
)