import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- 1. CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="Social Media Intelligence Dashboard",
    layout="wide"
)

# Custom CSS for Professional Styling & Square Buttons
st.markdown("""
<style>
    /* 1. Card styling for metrics */
    div[data-testid="stMetric"] {
        background-color: var(--secondary-background-color);
        border: 1px solid var(--text-color);
        padding: 15px;
        border-radius: 5px;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    }
    
    /* 2. Sidebar Background */
    section[data-testid="stSidebar"] {
        background-color: var(--secondary-background-color);
    }

    /* 3. SQUARE BUTTONS (Styling the Radio Selection) */
    div.row-widget.stRadio > div {
        flex-direction: column;
        align-items: stretch;
    }
    div.row-widget.stRadio > div[role="radiogroup"] > label {
        background-color: transparent;
        border: 1px solid var(--text-color);
        padding: 10px;
        margin-bottom: 5px;
        border-radius: 4px; 
        text-align: center;
        transition: background-color 0.3s;
    }
    div.row-widget.stRadio > div[role="radiogroup"] > label:hover {
        background-color: rgba(128, 128, 128, 0.1);
    }
    /* Highlight the selected button */
    div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"] > div:first-child {
        background-color: var(--primary-color);
        border-color: var(--primary-color);
    }
</style>
""", unsafe_allow_html=True)

# --- 2. DATA LOADING & PRE-PROCESSING ---
@st.cache_data
def load_and_prep_data():
    try:
        # Load Data
        df = pd.read_csv('Cleaned_Viral_Social_Media_Trends.csv')
        
        # Ensure Date Format
        if 'Post_Date' in df.columns:
            df['Post_Date'] = pd.to_datetime(df['Post_Date'])

        # --- DATA ENRICHMENT ---
        # 1. Total Interactions
        if 'Total_Interactions' not in df.columns:
            cols = [c for c in ['Likes', 'Shares', 'Comments'] if c in df.columns]
            df['Total_Interactions'] = df[cols].sum(axis=1)

        # 2. Engagement Rate
        if 'Engagement_Rate' not in df.columns:
            df['Engagement_Rate'] = (df['Total_Interactions'] / df['Views'].replace(0, 1)) * 100

        # 3. ROI Calculation (Simulated)
        if 'Ad_Spend' not in df.columns:
            df['Ad_Spend'] = (df['Views'] / 1000) * 5.00  
        
        if 'Revenue_Generated' not in df.columns:
            df['Revenue_Generated'] = (df['Total_Interactions'] * 0.50)

        if 'ROI' not in df.columns:
            df['ROI'] = ((df['Revenue_Generated'] - df['Ad_Spend']) / df['Ad_Spend'].replace(0, 1)) * 100

        return df

    except FileNotFoundError:
        return None

df = load_and_prep_data()

if df is None:
    st.error("Error: 'Cleaned_Viral_Social_Media_Trends.csv' not found.")
    st.stop()

# --- 3. SIDEBAR NAVIGATION & FILTERS ---
st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Go to:",
    ["Executive Overview", "Campaign & ROI Analysis", "Platform Performance", "Geographic Analytics", "Data Explorer"]
)

st.sidebar.markdown("---")
st.sidebar.header("Global Filters")

# Filters
selected_platform = st.sidebar.multiselect(
    "Filter by Platform",
    options=df['Platform'].unique(),
    default=[] 
)

selected_region = st.sidebar.multiselect(
    "Filter by Region",
    options=df['Region'].unique(),
    default=[]
)

# Apply Filter Logic
df_filtered = df.copy()

if selected_platform:
    df_filtered = df_filtered[df_filtered['Platform'].isin(selected_platform)]

if selected_region:
    df_filtered = df_filtered[df_filtered['Region'].isin(selected_region)]

# --- 4. MAIN DASHBOARD CONTENT ---

# === TAB 1: EXECUTIVE OVERVIEW ===
if page == "Executive Overview":
    st.title("Executive Overview")
    st.markdown("High-level performance metrics and key performance indicators (KPIs).")
    
    total_views = df_filtered['Views'].sum()
    avg_engagement_rate = df_filtered['Engagement_Rate'].mean()
    total_spend = df_filtered['Ad_Spend'].sum()
    avg_roi = df_filtered['ROI'].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Impressions", f"{total_views:,.0f}")
    col2.metric("Avg Engagement Rate", f"{avg_engagement_rate:.2f}%")
    col3.metric("Total Ad Spend (Est.)", f"${total_spend:,.2f}")
    col4.metric("Average ROI", f"{avg_roi:.2f}%")
    
    st.markdown("---")
    
    st.subheader("Performance Trends Over Time")
    if 'Post_Date' in df_filtered.columns:
        daily_trends = df_filtered.groupby('Post_Date')[['Views', 'Total_Interactions']].sum().reset_index()
        fig_line = px.line(daily_trends, x='Post_Date', y=['Views', 'Total_Interactions'], 
                           markers=True, template="plotly_white", 
                           title="Impressions vs. Interactions Timeline")
        fig_line.update_layout(height=450, legend_title_text='Metric')
        st.plotly_chart(fig_line, use_container_width=True)

# === TAB 2: CAMPAIGN & ROI ANALYSIS (IMPROVED) ===
elif page == "Campaign & ROI Analysis":
    st.title("Campaign Effectiveness & ROI")
    st.markdown("Analysis of campaign performance and return on investment.")
    
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.subheader("ROI by Content Category")
        roi_by_cat = df_filtered.groupby('Content_Type')[['ROI', 'Ad_Spend']].mean().reset_index()
        fig_bar_roi = px.bar(roi_by_cat, x='Content_Type', y='ROI', 
                             color='ROI', color_continuous_scale='RdBu',
                             title="Average Return on Investment (ROI) by Category")
        st.plotly_chart(fig_bar_roi, use_container_width=True)

    with c2:
        st.subheader("Cost Efficiency Analysis")
        
        # --- FIX: REMOVE EXTREME OUTLIERS FOR VISUALIZATION ---
        # We calculate the 95th percentile. Any ROI above this is likely an anomaly 
        # (or so high it skews the chart) and is hidden from this specific view.
        upper_limit = df_filtered['ROI'].quantile(0.95)
        lower_limit = df_filtered['ROI'].quantile(0.05)
        
        # Create a temporary dataframe just for this chart
        df_chart = df_filtered[
            (df_filtered['ROI'] < upper_limit) & 
            (df_filtered['ROI'] > lower_limit)
        ]
        
        fig_bubble = px.scatter(df_chart, 
                                x='Ad_Spend', 
                                y='ROI',
                                size='Views',
                                color='Content_Type',
                                hover_name='Hashtag',
                                title=f"Ad Spend vs. ROI (Outliers Removed)",
                                # Adding opacity helps see overlapping bubbles
                                opacity=0.7)
        
        # Add a zero line for reference
        fig_bubble.add_hline(y=0, line_dash="dash", line_color="gray")
        
        st.plotly_chart(fig_bubble, use_container_width=True)
        st.caption(f"Note: Extreme outliers (Top/Bottom 5%) removed to improve chart readability.")

    st.subheader("Top Performing Hashtags (Campaigns)")
    # We still use the full dataset here to show the true leaders
    top_campaigns = df_filtered.groupby('Hashtag')[['Views', 'Engagement_Rate', 'ROI']].mean().reset_index()
    top_campaigns = top_campaigns.sort_values(by='ROI', ascending=False).head(10)
    
    st.dataframe(
        top_campaigns.style.format({
            "Views": "{:,.0f}", 
            "Engagement_Rate": "{:.2f}", 
            "ROI": "{:.2f}"
        }), 
        use_container_width=True
    )
    
    # --- FIX START: Specific Formatting ---
    # We apply formatting only to specific numeric columns using a dictionary
    st.dataframe(
        top_campaigns.style.format({
            "Views": "{:,.0f}", 
            "Engagement_Rate": "{:.2f}", 
            "ROI": "{:.2f}"
        }), 
        use_container_width=True
    )
    # --- FIX END ---

# === TAB 3: PLATFORM PERFORMANCE ===
elif page == "Platform Performance":
    st.title("Platform Analytics")
    st.markdown("Comparative analysis of channel performance.")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Share of Voice")
        fig_pie = px.pie(df_filtered, names='Platform', values='Views', hole=0.5,
                         title="Distribution of Views by Platform")
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        st.subheader("Engagement Quality")
        fig_scatter = px.scatter(df_filtered, x='Views', y='Total_Interactions', color='Platform',
                                 title="Views vs. Total Interactions")
        st.plotly_chart(fig_scatter, use_container_width=True)

# === TAB 4: GEOGRAPHIC ANALYTICS ===
elif page == "Geographic Analytics":
    st.title("Geographic Distribution")
    
    st.subheader("Regional Performance Hierarchy")
    fig_tree = px.treemap(df_filtered, path=['Region', 'Platform'], values='Views',
                          color='Engagement_Rate', color_continuous_scale='Blues',
                          title="Views by Region (Color = Engagement Rate)")
    fig_tree.update_layout(height=600)
    st.plotly_chart(fig_tree, use_container_width=True)

# === TAB 5: DATA EXPLORER ===
elif page == "Data Explorer":
    st.title("Dataset Explorer")
    st.markdown("Detailed view of the filtered dataset.")
    
    st.dataframe(df_filtered, use_container_width=True)
    
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered CSV",
        data=csv,
        file_name='filtered_social_media_data.csv',
        mime='text/csv',
    )