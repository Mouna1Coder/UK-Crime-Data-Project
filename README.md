# 📊 UK Crime Data ETL Project

## 📌 Project Overview

This project fetches street-level crime data for London using the UK Police Data API, transforms it into a structured format, stores it in a MySQL database, and presents it in a simple interactive dashboard using Streamlit.

It follows the ETL (Extract, Transform, Load) process.

---

## ⚙️ Technologies Used

- Python
- Pandas
- Requests
- MySQL (Workbench or CLI)
- Streamlit
- UK Police Data API

---

## 🚀 How It Works

1. **Extract**: Data is pulled from the [UK Police API](https://data.police.uk/docs/) for London (using coordinates).
2. **Transform**: Unstructured JSON is converted into a clean Pandas DataFrame with relevant fields.
3. **Load**: The cleaned data is stored in a local MySQL database called `crime_data_api`, in a table named `crimes`.
4. **Visualise**: A simple Streamlit dashboard displays the data in table and chart format.

---

## 📁 Project Structure

UK_Crime_Data_Project/
│
├── crime_etl_pipeline.py # Main ETL script
├── streamlit_dashboard.py # Dashboard code
├── README.md # Project instructions (this file)
└── requirements.txt # (Optional) List of dependencies


---

## 🧪 How to Run the Project

### 1. Set up your MySQL database

- Open MySQL Workbench or CLI and run:

sql
CREATE DATABASE crime_data_api;

USE crime_data_api;

CREATE TABLE crimes (
  id VARCHAR(100) PRIMARY KEY,
  month VARCHAR(7),
  category VARCHAR(100),
  location_type VARCHAR(100),
  location_description VARCHAR(255),
  latitude FLOAT,
  longitude FLOAT,
  context TEXT,
  persistent_id VARCHAR(255),
  location_subtype VARCHAR(100)
);

### 2.Run the ETL Script 
python crime_etl_pipeline.py

You should see 
✅ Data fetched from API successfully.
✅ Records inserted into the database.
🔒 Database connection closed.

### 3.Run the Dashboard
streamlit run streamlit_dashboard.py

📦 (Optional) Create requirements.txt
pip freeze > requirements.txt

📝 Notes
This project uses made-up/generated data for learning purposes.

You can change the coordinates or date to fetch different results.

Make sure your MySQL server is running before executing the ETL.

💡 Why This Project?
To demonstrate understanding of:

APIs

Python and Pandas

Databases (MySQL)

ETL processes

Data visualisation with Streamlit









