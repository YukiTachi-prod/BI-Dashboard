Social Media Analytics Dashboard
A Streamlit dashboard for analyzing social media performance metrics and campaign effectiveness.

Features
Executive Overview: Key metrics and performance trends

ROI Analysis: Campaign effectiveness and cost efficiency

Platform Performance: Cross-channel comparison

Geographic Analytics: Regional performance mapping

Data Explorer: Raw data exploration and export

Quick Start
Install requirements:

pip install streamlit pandas plotly numpy

Place Cleaned_Viral_Social_Media_Trends.csv in the same directory

Run the dashboard:

streamlit run dashboard.py

Data Requirements
CSV file with columns: Platform, Region, Content_Type, Hashtag, Views, Likes, Shares, Comments, Post_Date

Usage
Use sidebar navigation to switch between analytical views

Apply filters by Platform and Region

Download filtered data from Data Explorer tab

Interactive charts support zoom and hover details

Technical Notes
Automatically calculates engagement metrics and ROI

Handles outliers in visualizations

Responsive design for all screen sizes

Local data processing only