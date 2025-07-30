# 🎮 Steam Game Marketplace Analysis
*Certification Bloc #4 — Data Science Training*

## 🚀 How to Access the Project

You can view the full Databricks notebook with all the analysis and visualizations here:

👉 [Databricks Project Link](https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/3399082203582185/655406070552781/4439945504723035/latest.html)

## 🎯 Project Objective

The objective of this project is to perform an in-depth analysis of the Steam videogame marketplace using big data tools. By leveraging PySpark and Databricks, we aim to transform a large, semi-structured dataset into meaningful insights that can guide business decisions in the gaming industry.

Specifically, this project seeks to:

- Understand the distribution of game genres and identify the most popular and profitable ones.
- Analyze publisher activity to determine who dominates the market and how release trends evolve over time.
- Examine the availability and support for different gaming platforms (Windows, Mac, Linux).
- Study pricing and discount strategies to reveal how they influence the market.
- Investigate language support across games to assess global accessibility.
- Provide actionable recommendations for game developers and publishers based on data-driven findings.

Ultimately, this project demonstrates the application of scalable data processing techniques to derive strategic insights from a complex and voluminous dataset, offering a valuable perspective for stakeholders like Ubisoft in planning future game developments and market entries.

## 🎯 Goal

The goal of this project is to leverage big data technologies to extract, transform, and analyze large-scale videogame data from Steam in order to uncover strategic market insights.

Through this analysis, we aim to:

- Identify market trends and patterns in game genres, pricing, discounts, and publisher activity.
- Understand the distribution of platform and language support among games.
- Reveal key factors that contribute to a game's market success.
- Provide data-driven recommendations that can help stakeholders — such as game developers, publishers, and investors — make informed decisions about game production and market positioning.

By achieving these goals, the project demonstrates the potential of big data analytics to drive smarter, evidence-based strategies in the dynamic and competitive videogame industry.

## 🔧 Tech Stack

- **PySpark**: For large-scale data processing and transformation, enabling efficient handling of semi-structured data.
- **Databricks**: A collaborative data platform that provides an interactive workspace for big data analytics and visualization.
- **AWS S3**: Storage of the raw, semi-structured JSON dataset used in this project.
- **Pandas**: (optional, for minor data handling): To complement PySpark for lightweight operations where appropriate.
- **Databricks Visualization Tools**: For creating insightful charts and graphs directly within the notebook.
- **Markdown**: For clear documentation and reporting within the notebook and on GitHub.

## 📌 Steps

To reproduce or understand the workflow of this project, follow these steps:

1. **Data Loading**:
   - Load the semi-structured JSON dataset from AWS S3 into a Databricks notebook using PySpark.

2. **Data Exploration**:
   - Inspect the schema to understand the nested structure of the dataset.
   - Flatten the nested fields using `select('data.*')` and prepare the data for transformation.

3. **Data Transformation**:
   - Clean the data by parsing timestamps, normalizing genres, handling missing values, and exploding arrays for more granular analysis.

4. **Exploratory Data Analysis (EDA)**:
   - Analyze key aspects such as publisher activity, genre popularity, platform distribution, price and discount trends, and language support.

5. **Data Visualization**:
   - Create visualizations using Databricks’ built-in tools to represent findings in an intuitive and actionable manner.

6. **Insights and Recommendations**:
   - Derive insights from the analysis to provide strategic recommendations for game development and publishing.

7. **Notebook Publication**:
   - Publish the Databricks notebook and generate a public link for sharing and review.

## 🚀 Next Steps

This project lays the foundation for deeper and more advanced analyses of the videogame marketplace. Possible future developments include:

- **Predictive Modeling**:
  - Build machine learning models to predict the success of a game based on its features (genre, price, platform, publisher reputation).
  
- **Sentiment Analysis**:
  - Incorporate user reviews and perform sentiment analysis to understand how player feedback correlates with sales and popularity.

- **Time Series Analysis**:
  - Analyze temporal trends in game releases and popularity over the years to predict emerging genres and market shifts.

- **Recommendation Systems**:
  - Develop a basic recommendation engine to suggest games to users based on their past preferences and market trends.

- **Benchmarking Across Platforms**:
  - Compare Steam data with other platforms (e.g., Epic Games Store, GOG) to gain a more holistic view of the digital gaming ecosystem.

- **Interactive Dashboards**:
  - Create a dynamic and interactive dashboard (using tools like Power BI, Tableau, or Databricks SQL) for real-time exploration of insights.

Each of these next steps would deepen the analytical value of the project and provide even richer strategic insights for stakeholders.


---

> 📌 *Project completed by Quentin Haentjens* — on April 26, 2025, as part of my training at Jedha.

