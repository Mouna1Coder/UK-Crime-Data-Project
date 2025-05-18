import streamlit as st
import pandas as pd
import mysql.connector

# Connect to the database
def get_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="username",
        password="password",
        database="crime_data_api"
    )
    query = "SELECT * FROM crimes"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Streamlit UI
st.title("📊 UK Crime Data Dashboard")
st.markdown("Showing crime data from the Police API.")

# Load data
df = get_data()

# Filters
categories = df['category'].dropna().unique()
selected_category = st.selectbox("Select a crime category", options=sorted(categories))

filtered_df = df[df['category'] == selected_category]

# Show results
st.subheader(f"Total records for category: **{selected_category}**")
st.write(f"Total crimes: {len(filtered_df)}")
st.dataframe(filtered_df)

# Optional: Show top locations
top_locations = filtered_df['location_description'].value_counts().head(5)
st.subheader("Top 5 Locations for This Category")
st.bar_chart(top_locations)
