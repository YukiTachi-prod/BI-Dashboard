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

# --- 2. CSS STYLING ---
st.markdown("""
<style>
    /* 1. Global Metrics Card Styling */
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

    /* --- 3. CUSTOM SIDEBAR BUTTON STYLING --- */
    
    /* Target ONLY buttons inside the Sidebar */
    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;             /* Make buttons fill the column/container */
        border-radius: 4px;      /* Slight rounding */
        height: 3em;             /* Fixed height for uniformity */
        font-weight: 600;
        border: 1px solid rgba(128, 128, 128, 0.3);
        transition: all 0.2s ease-in-out;
    }

    /* Styling for the Unselected (Secondary) Buttons */
    section[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
        background-color: #ffffff;
        color: #31333F;
    }

    /* Styling for the Selected (Primary) Buttons - The "Active" Red State */
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background-color: #FF4B4B !important;
        border-color: #FF4B4B !important;
        color: white !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    /* Hover effects */
    section[data-testid="stSidebar"] .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

</style>
""", unsafe_allow_html=True)

# --- 3. DATA LOADING & PRE-PROCESSING ---
@st.cache_data
def load_and_prep_data():
    try:
        # Load Data
        df = pd.read_csv('Cleaned_Viral_Social_Media_Trends.csv')
        
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

# Initialize Session State for Regions if it doesn't exist
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

# 1. "All Regions" Button (Top Center)
# If list is empty, "All Regions" is active (Primary color)
all_regions_active = len(st.session_state.selected_regions) == 0
if st.sidebar.button("All Regions", 
                     type="primary" if all_regions_active else "secondary", 
                     use_container_width=True):
    clear_regions()
    st.rerun()

# 2. Country Grid (Middle - 2 Columns)
unique_regions = sorted(list(df['Region'].unique()))

# Create columns for grid layout
col1, col2 = st.sidebar.columns(2)

for i, region in enumerate(unique_regions):
    # Determine if this specific region is selected (for color styling)
    is_selected = region in st.session_state.selected_regions
    button_type = "primary" if is_selected else "secondary"
    
    # Alternate columns based on index (Evens in col1, Odds in col2)
    with col1 if i % 2 == 0 else col2:
        if st.button(region, key=f"btn_{region}", type=button_type, use_container_width=True):
            toggle_region(region)
            st.rerun()

# 3. Clear Button (Bottom Center)
st.sidebar.markdown("<br>", unsafe_allow_html=True) # Add a little space
if st.sidebar.button("Clear Selection", use_container_width=True):
    clear_regions()
    st.rerun()


# --- 5. APPLY FILTER LOGIC ---
df_filtered = df.copy()

if selected_platform:
    df_filtered = df_filtered[df_filtered['Platform'].isin(selected_platform)]

# If specific regions are selected in state, filter by them.
# If list is empty [], it means "All Regions", so we do NOT filter.
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
                           markers=True, template="plotly_white", 
                           title="Impressions vs. Interactions Timeline")
        fig_line.update_layout(height=450, legend_title_text='Metric')
        st.plotly_chart(fig_line, use_container_width=True)

# === TAB 2: CAMPAIGN & ROI ANALYSIS ===
with tab2:
    st.header("Campaign Effectiveness & ROI")
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
        
        upper_limit = df_filtered['ROI'].quantile(0.95)
        lower_limit = df_filtered['ROI'].quantile(0.05)
        
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
                                opacity=0.7)
        
        fig_bubble.add_hline(y=0, line_dash="dash", line_color="gray")
        
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
        fig_pie = px.pie(df_filtered, names='Platform', values='Views', hole=0.5,
                         title="Distribution of Views by Platform")
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        st.subheader("Engagement Quality")
        fig_scatter = px.scatter(df_filtered, x='Views', y='Total_Interactions', color='Platform',
                                 title="Views vs. Total Interactions")
        st.plotly_chart(fig_scatter, use_container_width=True)

# === TAB 4: GEOGRAPHIC ANALYTICS ===
with tab4:
    st.header("Geographic Distribution")
    
    st.subheader("Regional Performance Hierarchy")
    fig_tree = px.treemap(df_filtered, path=['Region', 'Platform'], values='Views',
                          color='Engagement_Rate', color_continuous_scale='Blues',
                          title="Views by Region (Color = Engagement Rate)")
    fig_tree.update_layout(height=600)
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