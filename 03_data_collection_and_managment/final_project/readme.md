# 🧭 Weather-Based Destination Recommender — Kayak x Booking
*Certification Bloc #3 — Data Science Training*

## 🎯 Project Objective

This project aims to help users choose the **best travel destinations in France** based on the **upcoming weather** and the **quality of available hotels**.

By combining **7-day weather forecasts** with hotel data from **Booking.com**, we compute a custom **weather comfort score** that ranks cities from best to worst conditions — allowing users (or platforms like Kayak) to surface the most attractive locations dynamically.

The project ends with two **interactive Mapbox visualizations**:
- A map of the **Top 5 French cities** based on weather comfort
- A map of the **Top 20 best-rated hotels** in those cities

---

## 🎯 Goal

Build a full pipeline to collect, combine, and visualize:
- 7-day weather data for 35 major French cities  
- Hotel data scraped from Booking.com  
- A custom **comfort score** based on feels-like temperature, rainfall, and wind  
- A smart destination/hotel recommender powered by data  

---

## 🔧 Tech Stack

- **Python 3.10**
- **Scrapy** for web scraping (Booking.com)
- **Pandas** & **Plotly Express** for analysis & visualization
- **AWS S3** for CSV storage
- **PostgreSQL on AWS RDS** for database storage
- **SQLAlchemy** + `psycopg2` for database connection
- `.env` + hidden secret config folder for credentials

---

## 📌 Steps

### 1. Weather data
- Collect weather forecasts via the **OpenWeather API** for 35 cities
- Compute a **comfort score**: temperature − rain − wind penalty
- Save to `weather.csv`

### 2. Hotel data
- Scrape hotel listings on Booking.com using **Scrapy**
- For each hotel: name, stars, rating, description, link, coordinates (from hotel page)
- Save to `hotels.json` and `hotels.csv`

### 3. Data fusion
- Merge hotel and weather data into `weather_and_hotels.csv`
- One row = one hotel, with attached weather data of its city

### 4. Cloud storage & database
- Upload the merged CSV to a dedicated **AWS S3 bucket**
- Create a PostgreSQL database on **AWS RDS**
- Send the final dataset to a table via `SQLAlchemy`

### 5. Visualization
- Import the data from RDS
- Generate two **interactive Mapbox maps**:
  - **Top 5 cities** with the best weather score
  - **Top 20 hotels** among those cities

---

## 🗺️ Outputs

### Top 5 Weather Destinations (Map)
An interactive map showing the 5 French cities with the highest comfort score over the next 7 days.  
- Color: weather score  
- Hover: temperature, rain  
- Fully zoomed and centered based on data

### Top 20 Hotels (Map)
A map of the best-rated hotels (Booking rating) located in those cities.  
- Hover shows name, city, and rating  
- Each marker corresponds to a real hotel from Booking.com

---

## 📍 Insights

- The **south of France** is generally overrepresented among the top cities  
- Booking shows a strong **alignment between favorable weather zones and high-rated hotels**  
- This data could power a smart recommendation engine on a travel platform

---

## 🚀 Next Steps

- Add **pricing information** and filter by budget  
- Create a **Streamlit interface** for user interaction  
- Deploy an internal API to serve top destinations dynamically

---
> 📌 *Project completed by Quentin Haentjens* — on May 22, 2025, as part of my training at Jedha.
