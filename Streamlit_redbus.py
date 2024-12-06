import streamlit as st
import pymysql
import pandas as pd

# Function to connect to the MySQL database
def get_connection():
    return pymysql.connect(
        host="localhost",
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

# Function to fetch filtered data from the database
def fetch_bus_routes(route_name=None, price_range=None, star_rating=None, bus_type=None, departing_time=None):
    query = "SELECT * FROM bus_routes WHERE 1=1"
    params = []

    if route_name and route_name != "All Routes":
        query += " AND Route_Name = %s"
        params.append(route_name)

    if price_range:
        query += " AND Price BETWEEN %s AND %s"
        params.extend(price_range)

    if star_rating:
        query += " AND Star_Rating >= %s"
        params.append(star_rating)

    if bus_type and bus_type != "All Bus Types":
        query += " AND Bus_Type = %s"
        params.append(bus_type)

    if departing_time:
        query += " AND Departing_Time >= %s"  # Adjusted column name to Departing_Time
        params.append(departing_time)

    conn = get_connection()
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df


# Streamlit app interface
st.title("RedBus Routes Viewer")
st.write("This app interacts with the RedBus database to fetch and display bus routes with advanced filtering.")

# Main interface: Route selection
unique_route_names = fetch_unique_route_names()
selected_route_name = st.selectbox("Select a Route Name:", options=["All Routes"] + unique_route_names)

# Sidebar for filters
st.sidebar.header("Filters")

# Price range filter
price_min, price_max = st.sidebar.slider("Select Price Range:", min_value=0, max_value=5000, value=(0, 5000), step=100)

# Star rating filter
selected_star_rating = st.sidebar.slider("Minimum Star Rating:", min_value=0.0, max_value=5.0, value=0.0, step=0.5)

# Bus type filter (changed from Seat_Type to Bus_Type)
bus_types = ["All Bus Types", "AC", "Non-AC", "Sleeper", "Semi-Sleeper", "Seater"]  # Adjust according to your data
selected_bus_type = st.sidebar.selectbox("Select Bus Type:", options=bus_types)

# Departure time filter (changed label to "Departing Time")
selected_departure_time = st.sidebar.time_input("Select Departing Time:", value=None)

# Convert selected_departure_time to a string format for SQL query
if selected_departure_time:
    selected_departure_time = str(selected_departure_time)

# Fetch data based on filters
data = fetch_bus_routes(
    route_name=selected_route_name,
    price_range=(price_min, price_max),
    star_rating=selected_star_rating,
    bus_type=selected_bus_type,
    departing_time=selected_departure_time
)

# Display data in a table
if not data.empty:
    st.dataframe(data)
else:
    st.write("No routes found for the selected filters.")

# Option to download data
csv = data.to_csv(index=False)
st.download_button(
    label="Download Data as CSV",
    data=csv,
    file_name="bus_routes.csv",
    mime="text/csv"
)
