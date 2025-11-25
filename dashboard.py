import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="Social Media Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for a professional "Front End" look
st.markdown("""
<style>
    /* Card styling for metrics */
    div[data-testid="stMetric"] {
        background-color: #F8F9FA;
        border: 1px solid #E6E9EF;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        text-align: center;
    }
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #2E4053;
        color: white;
    }
    /* Sidebar text color fix if needed */
    .css-1d391kg {
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. DATA LOADING ---
@st.cache_data
def load_data():
    df = pd.read_csv('Cleaned_Viral_Social_Media_Trends.csv')
    if 'Post_Date' in df.columns:
        df['Post_Date'] = pd.to_datetime(df['Post_Date'])
    return df

try:
    df = load_data()
except Exception as e:
    st.error("Error loading data. Please ensure 'Cleaned_Viral_Social_Media_Trends.csv' is in the directory.")
    st.stop()

# --- 3. SIDEBAR NAVIGATION (LEFT PANEL TABS) ---
st.sidebar.title("📱 Menu")

# This Radio button acts as the "Tabs" on the left
page = st.sidebar.radio(
    "Select Category:",
    ["Overview", "Platform Analysis", "Content Insights", "Regional Analytics", "Raw Data"]
)

st.sidebar.markdown("---")
st.sidebar.header("🔍 Global Filters")
st.sidebar.info("These filters apply to all tabs.")

# Filters
selected_platform = st.sidebar.multiselect(
    "Filter by Platform",
    options=df['Platform'].unique(),
    default=df['Platform'].unique()
)

selected_region = st.sidebar.multiselect(
    "Filter by Region",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

# Apply Filters
df_filtered = df[
    (df['Platform'].isin(selected_platform)) & 
    (df['Region'].isin(selected_region))
]

# --- 4. MAIN CONTENT AREA (CHANGES BASED ON TAB) ---

# === TAB 1: OVERVIEW ===
if page == "Overview":
    st.title("🚀 Executive Overview")
    st.markdown("High-level performance metrics across all social channels.")
    
    # Top KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Views", f"{df_filtered['Views'].sum():,.0f}", delta="Accumulated")
    col2.metric("Total Likes", f"{df_filtered['Likes'].sum():,.0f}")
    col3.metric("Avg Shares", f"{df_filtered['Shares'].mean():,.0f}")
    col4.metric("Top Engagement", df_filtered['Engagement_Level'].mode()[0])
    
    st.markdown("---")
    
    # Main Trend Chart
    st.subheader("📅 Engagement Trends Over Time")
    if 'Post_Date' in df_filtered.columns:
        daily_trends = df_filtered.groupby('Post_Date')[['Views', 'Likes']].sum().reset_index()
        fig_line = px.line(daily_trends, x='Post_Date', y=['Views', 'Likes'], 
                           markers=True, template="plotly_white", title="Views & Likes Timeline")
        fig_line.update_layout(height=400)
        st.plotly_chart(fig_line, use_container_width=True)

# === TAB 2: PLATFORM ANALYSIS ===
elif page == "Platform Analysis":
    st.title("📊 Platform Performance")
    st.markdown("Compare how different social media apps are performing.")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Share of Voice (Views)")
        fig_pie = px.pie(df_filtered, names='Platform', values='Views', hole=0.4,
                         title="Views Distribution by Platform")
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        st.subheader("Engagement Quality")
        # Scatter plot to show correlation
        fig_scatter = px.scatter(df_filtered, x='Views', y='Likes', color='Platform',
                                 size='Shares', hover_data=['Content_Type'],
                                 title="Views vs. Likes Correlation")
        st.plotly_chart(fig_scatter, use_container_width=True)

# === TAB 3: CONTENT INSIGHTS ===
elif page == "Content Insights":
    st.title("📝 Content Strategy")
    st.markdown("Analyze which types of content generate the most buzz.")
    
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("Performance by Content Type")
        # Grouped Bar Chart
        avg_metrics = df_filtered.groupby('Content_Type')[['Likes', 'Shares', 'Comments']].mean().reset_index()
        avg_melt = avg_metrics.melt(id_vars='Content_Type', value_vars=['Likes', 'Shares', 'Comments'])
        
        fig_bar = px.bar(avg_melt, x='Content_Type', y='value', color='variable', barmode='group',
                         template="plotly_white", title="Average Interactions per Content Type")
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with c2:
        st.subheader("Top Hashtags")
        top_hash = df_filtered.groupby('Hashtag')['Views'].sum().nlargest(10).reset_index().sort_values('Views')
        fig_hash = px.bar(top_hash, x='Views', y='Hashtag', orientation='h',
                          template="plotly_white", color='Views')
        st.plotly_chart(fig_hash, use_container_width=True)

# === TAB 4: REGIONAL ANALYTICS ===
elif page == "Regional Analytics":
    st.title("🌍 Geographic Distribution")
    
    st.subheader("Where are the views coming from?")
    # Treemap is excellent for hierarchical data (Region -> Platform)
    fig_tree = px.treemap(df_filtered, path=['Region', 'Platform'], values='Views',
                          color='Views', color_continuous_scale='Viridis',
                          title="Views Breakdown by Region and Platform")
    fig_tree.update_layout(height=600)
    st.plotly_chart(fig_tree, use_container_width=True)

# === TAB 5: RAW DATA ===
elif page == "Raw Data":
    st.title("📂 Dataset Explorer")
    st.markdown("Inspect the raw data used for this analysis.")
    
    st.dataframe(df_filtered, use_container_width=True)
    
    # Download Button
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name='filtered_social_media_data.csv',
        mime='text/csv',
    )