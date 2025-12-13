import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# config
st.set_page_config(
    page_title="Social Media Intelligence Dashboard",
    layout="wide"
)

# ui theme
st.markdown("""
<style>
    /* IMPORT FONT - 'Nunito' matches the rounded, friendly vibe */
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }

    /* A. MAIN BACKGROUND */
    .stApp {
        background-color: #F4F7F6; /* Very light cool grey/green tint */
    }
    
    /* FORCE BLACK TEXT FOR ALL ELEMENTS (Override Dark Mode) */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    .stApp p, .stApp span, .stApp div, .stApp label,
    .stMarkdown, .stMarkdown p, .stMarkdown span,
    .stDataFrame, .stDataFrame td, .stDataFrame th,
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stText"],
    .element-container {
        color: #000000 !important;
    }
    
    /* Force black text in dataframes */
    .dataframe, .dataframe tbody tr td, .dataframe thead tr th {
        color: #000000 !important;
    }
    
    /* Force black text in tabs */
    .stTabs [data-baseweb="tab"] {
        color: #000000 !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: #4CAF50 !important;
    }

    /* B. SIDEBAR STYLING (Green Gradient) */
    section[data-testid="stSidebar"] {
        /* The Gradient: Starts with Vibrant Green, flows into Deep Forest/Teal */
        background: linear-gradient(180deg, #4CAF50 0%, #2E7D32 100%);
        box-shadow: 5px 0 15px rgba(46, 125, 50, 0.3);
    }
    
    /* Sidebar Text Color */
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: white !important;
        letter-spacing: 0.5px;
    }

    /* C. METRIC CARDS (White floating cards) */
    div[data-testid="stMetric"] {
        background: white;
        border-radius: 20px; /* Highly rounded corners */
        padding: 20px;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05); /* Soft diffuse shadow */
        border: none;
    }

    /* Metric Label styling */
    div[data-testid="stMetric"] label {
        color: #8898aa; /* Muted grey */
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    /* Metric Value styling */
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #2D3436; /* Dark charcoal text */
        font-weight: 800;
    }

    /* D. BUTTON STYLING (The Region Toggles) */
    
    /* 1. Unselected Buttons (Translucent White on Gradient Sidebar) */
    section[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
        background-color: rgba(255, 255, 255, 0.15); /* Glass effect */
        color: white !important;
        border: 1px solid rgba(255,255,255, 0.2);
        border-radius: 12px; 
        height: 3em;
        font-weight: 700;
        backdrop-filter: blur(5px); /* Blurs the gradient behind the button */
        transition: background-color 0.2s ease, color 0.2s ease;
    }
    
    section[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
        background-color: rgba(255,255,255, 0.3);
    }
    
    /* Force white text for unselected buttons */
    section[data-testid="stSidebar"] .stButton > button[kind="secondary"] p,
    section[data-testid="stSidebar"] .stButton > button[kind="secondary"] span,
    section[data-testid="stSidebar"] .stButton > button[kind="secondary"] div {
        color: white !important;
    }

    /* 2. Selected Buttons (Pure White with Black Text) */
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background-color: white !important;
        border: none !important;
        color: #000000 !important; /* Black text for selected buttons */
        border-radius: 12px;
        height: 3em;
        font-weight: 800;
        transition: background-color 0.2s ease, color 0.2s ease;
    }

    section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
        background-color: #F1F8E9 !important;
        color: #000000 !important; /* Keep black text on hover */
    }
    
    /* Force black text for selected buttons - target all child elements */
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] p,
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] span,
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] div {
        color: #000000 !important;
    }

    /* E. TAB STYLING (Top Navigation) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: white;
        border-radius: 15px 15px 0px 0px;
        gap: 1px;
        padding: 10px 20px;
        color: #000000 !important;
        border: none;
        font-weight: 600;
        box-shadow: 0 -2px 5px rgba(0,0,0,0.02);
    }

    .stTabs [aria-selected="true"] {
        background-color: white;
        color: #4CAF50 !important; /* Active tab is Green */
        border-bottom: 4px solid #4CAF50;
    }
    
    /* Force black text in tab content */
    .stTabs [data-baseweb="tab-panel"] * {
        color: #000000 !important;
    }
    
    /* Except for sidebar which stays white */
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* But sidebar labels and text inputs need special handling */
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p {
        color: white !important;
    }

    /* F. PLOTLY CHART CONTAINERS */
    .stPlotlyChart {
        background-color: white;
        border-radius: 20px;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
        padding: 15px;
    }
    
    /* Force Plotly chart text to be black */
    .stPlotlyChart text {
        fill: #000000 !important;
    }
    
    .js-plotly-plot .plotly text {
        fill: #000000 !important;
    }
    
    /* G. CLEANUP */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    .stMultiSelect label {
        color: white !important;
    }
    
    .stMultiSelect div[data-baseweb="tag"] {
        background-color: rgba(255,255,255,0.9);
    }
            
    @media (prefers-color-scheme: dark) {
    html, body, .stApp, [class*="css"] {
        background: #F4F7F6 !important;
        color: #000000 !important;
    }
}
</style>
""", unsafe_allow_html=True)

# --- 3. DATA LOADING & PRE-PROCESSING ---
@st.cache_data
def load_and_prep_data():
    try:
        # Load Data
        df = pd.read_csv('src/Cleaned_Viral_Social_Media_Trends.csv')
        
        # Ensure Date Format
        if 'Post_Date' in df.columns:
            df['Post_Date'] = pd.to_datetime(df['Post_Date'])

        # --- DATA ENRICHMENT ---
        if 'Total_Interactions' not in df.columns:
            cols = [c for c in ['Likes', 'Shares', 'Comments'] if c in df.columns]
            df['Total_Interactions'] = df[cols].sum(axis=1)

        if 'Engagement_Rate' not in df.columns:
            df['Engagement_Rate'] = (df['Total_Interactions'] / df['Views'].replace(0, 1)) * 100

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

# --- UPDATE PLOTLY DEFAULTS FOR HIGH CONTRAST ---
px.defaults.template = "plotly_white"

# High Contrast Palette: Green, Blue, Orange, Purple, Red, Cyan
# This ensures lines/bars are NOT similar in color
px.defaults.color_discrete_sequence = [
    "#4CAF50", # Green (Primary)
    "#2196F3", # Blue
    "#FF9800", # Orange
    "#9C27B0", # Purple
    "#F44336", # Red
    "#00BCD4"  # Cyan
]

# --- 4. SIDEBAR LOGIC (SESSION STATE & BUTTONS) ---
st.sidebar.header("Filter Settings")

# 4A. Platform Filter
selected_platform = st.sidebar.multiselect(
    "Filter by Platform",
    options=df['Platform'].unique(),
    default=[] 
)

st.sidebar.markdown("---")
st.sidebar.subheader("Select Region")

# Initialize Session State for Regions
if 'selected_regions' not in st.session_state:
    st.session_state.selected_regions = []

# --- FUNCTION TO HANDLE TOGGLES ---
def toggle_region(region_name):
    if region_name in st.session_state.selected_regions:
        st.session_state.selected_regions.remove(region_name)
    else:
        st.session_state.selected_regions.append(region_name)

def clear_regions():
    st.session_state.selected_regions = []

# --- RENDER BUTTONS ---

# 1. "All Regions" Button
all_regions_active = len(st.session_state.selected_regions) == 0
if st.sidebar.button("All Regions", 
                     type="primary" if all_regions_active else "secondary", 
                     use_container_width=True):
    clear_regions()
    st.rerun()

# 2. Country Grid (Middle - 2 Columns)
unique_regions = sorted(list(df['Region'].unique()))

col1, col2 = st.sidebar.columns(2)

for i, region in enumerate(unique_regions):
    is_selected = region in st.session_state.selected_regions
    button_type = "primary" if is_selected else "secondary"
    
    with col1 if i % 2 == 0 else col2:
        if st.button(region, key=f"btn_{region}", type=button_type, use_container_width=True):
            toggle_region(region)
            st.rerun()

# 3. Clear Button
st.sidebar.markdown("<br>", unsafe_allow_html=True)
if st.sidebar.button("Clear Selection", use_container_width=True):
    clear_regions()
    st.rerun()


# --- 5. APPLY FILTER LOGIC ---
df_filtered = df.copy()

if selected_platform:
    df_filtered = df_filtered[df_filtered['Platform'].isin(selected_platform)]

if st.session_state.selected_regions:
    df_filtered = df_filtered[df_filtered['Region'].isin(st.session_state.selected_regions)]

# --- 6. MAIN DASHBOARD CONTENT ---

st.title("Social Media Intelligence Dashboard")

# Create Horizontal Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Executive Overview", 
    "Campaign & ROI Analysis", 
    "Platform Performance", 
    "Geographic Analytics", 
    "Data Explorer"
])

# === TAB 1: EXECUTIVE OVERVIEW ===
with tab1:
    st.header("Executive Overview")
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
                           markers=True, 
                           title="Impressions vs. Interactions Timeline")
        
        # Ensure lines are distinct colors (Green vs Blue/Orange)
        fig_line.update_layout(
            height=450, 
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            font_family="Nunito",
            font_color="#000000"  # Force black text
        )
        fig_line.update_xaxes(showgrid=False)
        fig_line.update_yaxes(showgrid=True, gridcolor='#ECEFF1')
        st.plotly_chart(fig_line, use_container_width=True)

# === TAB 2: CAMPAIGN & ROI ANALYSIS ===
with tab2:
    st.header("Campaign Effectiveness & ROI")
    st.markdown("Analysis of campaign performance and return on investment.")
    
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.subheader("ROI by Content Category")
        roi_by_cat = df_filtered.groupby('Content_Type')[['ROI', 'Ad_Spend']].mean().reset_index()
        
        # CHANGED: Color by 'Content_Type' (categorical) instead of 'ROI' (numeric)
        # This forces distinct colors for each bar instead of similar greens
        fig_bar_roi = px.bar(roi_by_cat, x='Content_Type', y='ROI', 
                             color='Content_Type', # <--- Distinct Colors!
                             title="Average Return on Investment (ROI) by Category")
        
        fig_bar_roi.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)', 
            font_family="Nunito",
            font_color="#000000"
        )
        st.plotly_chart(fig_bar_roi, use_container_width=True)

    with c2:
        st.subheader("Cost Efficiency Analysis")
        
        upper_limit = df_filtered['ROI'].quantile(0.95)
        lower_limit = df_filtered['ROI'].quantile(0.05)
        
        df_chart = df_filtered[
            (df_filtered['ROI'] < upper_limit) & 
            (df_filtered['ROI'] > lower_limit)
        ]
        
        # Scatter plot uses the new diverse color palette
        fig_bubble = px.scatter(df_chart, 
                                x='Ad_Spend', 
                                y='ROI',
                                size='Views',
                                color='Content_Type',
                                hover_name='Hashtag',
                                title=f"Ad Spend vs. ROI (Outliers Removed)",
                                opacity=0.8)
        
        fig_bubble.add_hline(y=0, line_dash="dash", line_color="#B0BEC5")
        fig_bubble.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)', 
            font_family="Nunito",
            font_color="#000000"
        )
        
        st.plotly_chart(fig_bubble, use_container_width=True)
        st.caption(f"Note: Extreme outliers (Top/Bottom 5%) removed to improve chart readability.")

    st.subheader("Top Performing Hashtags (Campaigns)")
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

# === TAB 3: PLATFORM PERFORMANCE ===
with tab3:
    st.header("Platform Analytics")
    st.markdown("Comparative analysis of channel performance.")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Share of Voice")
        # Pie chart will now automatically use the Green/Blue/Orange/Purple/Red mix
        fig_pie = px.pie(df_filtered, names='Platform', values='Views', hole=0.5,
                         title="Distribution of Views by Platform")
        fig_pie.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)', 
            font_family="Nunito",
            font_color="#000000"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        st.subheader("Engagement Quality")
        fig_scatter = px.scatter(df_filtered, x='Views', y='Total_Interactions', color='Platform',
                                 title="Views vs. Total Interactions")
        fig_scatter.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)', 
            font_family="Nunito",
            font_color="#000000"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

# === TAB 4: GEOGRAPHIC ANALYTICS ===
with tab4:
    st.header("Geographic Distribution")
    
    st.subheader("Regional Performance Hierarchy")
    # Using 'Viridis' ensures the treemap boxes aren't all just green
    # Added explicit font color to ensure visibility
    fig_tree = px.treemap(df_filtered, path=['Region', 'Platform'], values='Views',
                          color='Engagement_Rate', color_continuous_scale='Viridis',
                          title="Views by Region (Color = Engagement Rate)")
    fig_tree.update_layout(
        height=600, 
        font_family="Nunito",
        font_color="#000000",  # Force black text
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    fig_tree.update_traces(
        textfont=dict(color='#000000', size=12),  # Ensure text is visible
        marker=dict(line=dict(color='#FFFFFF', width=2))  # White borders for better separation
    )
    st.plotly_chart(fig_tree, use_container_width=True)

# === TAB 5: DATA EXPLORER ===
with tab5:
    st.header("Dataset Explorer")
    st.markdown("Detailed view of the filtered dataset.")
    
    st.dataframe(df_filtered, use_container_width=True)
    
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered CSV",
        data=csv,
        file_name='filtered_social_media_data.csv',
        mime='text/csv',
    )