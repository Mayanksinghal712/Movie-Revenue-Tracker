import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from datetime import datetime
import numpy as np

# ==============================================================================
# PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Movie Revenue Tracker - Regional Analysis",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# CSS STYLING CONFIGURATION
# ==============================================================================
def load_custom_css():
    """Load custom CSS for better visual design and color contrast"""
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
        
        /* === CSS VARIABLES === */
        :root {
            --primary-bg: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            --secondary-bg: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --accent-color: #4facfe;
            --success-color: #43e97b;
            --warning-color: #f093fb;
            
            --glass-bg: rgba(255, 255, 255, 0.15);
            --glass-border: rgba(255, 255, 255, 0.25);
            --dark-glass: rgba(0, 0, 0, 0.1);
            
            --text-primary: #ffffff;
            --text-secondary: rgba(255, 255, 255, 0.85);
            --text-accent: #4facfe;
            --text-dark: #2c3e50;
            
            --shadow-soft: 0 8px 32px rgba(31, 38, 135, 0.37);
            --shadow-strong: 0 15px 50px rgba(0, 0, 0, 0.4);
            --border-radius: 20px;
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        /* === GLOBAL STYLES === */
        .main .block-container {
            padding-top: 1rem;
            max-width: 1200px;
        }
        
        .stApp {
            background: var(--primary-bg);
            background-attachment: fixed;
            color: var(--text-primary);
        }
        
        /* Hide Default Elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        /* === TYPOGRAPHY === */
        .main-header {
            text-align: center;
            color: var(--text-primary);
            font-size: 4rem;
            margin: 2rem 0;
            font-weight: 800;
            font-family: 'Poppins', sans-serif;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
            animation: headerGlow 3s ease-in-out infinite alternate;
        }
        
        @keyframes headerGlow {
            from { 
                filter: drop-shadow(0 0 10px rgba(255,255,255,0.3));
                transform: scale(1);
            }
            to { 
                filter: drop-shadow(0 0 20px rgba(255,255,255,0.6));
                transform: scale(1.02);
            }
        }
        
        .sub-header {
            text-align: center;
            color: var(--text-secondary);
            font-size: 1.4rem;
            margin-bottom: 3rem;
            font-weight: 400;
            font-family: 'Poppins', sans-serif;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.4);
        }
        
        /* === METRIC CARDS === */
        .metric-card {
            background: var(--glass-bg);
            backdrop-filter: blur(20px) saturate(180%);
            border: 1px solid var(--glass-border);
            padding: 2rem 1.5rem;
            border-radius: var(--border-radius);
            color: var(--text-primary);
            text-align: center;
            box-shadow: var(--shadow-soft);
            transition: var(--transition);
            margin-bottom: 1rem;
            font-family: 'Poppins', sans-serif;
            position: relative;
            overflow: hidden;
        }
        
        .metric-card:hover {
            transform: translateY(-10px) scale(1.02);
            box-shadow: var(--shadow-strong);
            border-color: rgba(255, 255, 255, 0.4);
        }
        
        .metric-card h3 {
            font-size: 3rem;
            margin-bottom: 1rem;
            color: var(--text-primary);
            filter: drop-shadow(0 0 10px rgba(255,255,255,0.5));
        }
        
        .metric-card h2 {
            font-size: 2.2rem;
            margin: 1rem 0;
            font-weight: 700;
            color: var(--text-accent);
            text-shadow: 0 0 10px rgba(79, 172, 254, 0.5);
        }
        
        .metric-card p {
            font-size: 1rem;
            margin: 0;
            color: var(--text-secondary);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* === FORM CONTROLS === */
        .stSelectbox label, .stSlider label, .stNumberInput label, .stRadio label {
            color: var(--text-primary) !important;
            font-weight: 600 !important;
            font-family: 'Poppins', sans-serif !important;
        }
        
        .stSelectbox > div > div {
            background: var(--glass-bg);
            backdrop-filter: blur(10px);
            border: 1px solid var(--glass-border);
            border-radius: 15px;
            color: var(--text-primary);
            font-family: 'Poppins', sans-serif;
        }
        
        .stRadio > div {
            color: var(--text-primary) !important;
        }
        
        /* === TABS === */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            padding: 1rem;
            border-radius: var(--border-radius);
            border: 1px solid var(--glass-border);
            box-shadow: var(--shadow-soft);
        }
        
        .stTabs [data-baseweb="tab"] {
            background: var(--dark-glass);
            color: var(--text-primary);
            border-radius: 15px;
            font-weight: 600;
            font-family: 'Poppins', sans-serif;
            padding: 1rem 2rem;
            border: 1px solid var(--glass-border);
            transition: var(--transition);
        }
        
        .stTabs [aria-selected="true"] {
            background: var(--accent-color);
            color: var(--text-primary);
            font-weight: 700;
            transform: translateY(-2px);
            box-shadow: var(--shadow-soft);
        }
        
        /* === TEXT VISIBILITY FIXES === */
        .stMarkdown p, .stMarkdown div, .stText {
            color: var(--text-primary) !important;
        }
        
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
            color: var(--text-primary) !important;
        }
        
        /* === ANALYSIS HEADERS === */
        .analysis-header {
            color: var(--text-accent);
            font-size: 3rem;
            font-weight: 800;
            margin: 2rem 0;
            font-family: 'Poppins', sans-serif;
            text-align: center;
            text-shadow: 0 0 15px rgba(79, 172, 254, 0.6);
        }
        
        /* === RESPONSIVE DESIGN === */
        @media (max-width: 768px) {
            .main-header { font-size: 2.5rem; }
            .metric-card { padding: 1.5rem 1rem; }
            .analysis-header { font-size: 2rem; }
        }
    </style>
    """

# Apply Custom CSS
st.markdown(load_custom_css(), unsafe_allow_html=True)

# ==============================================================================
# DATA LOADING AND PROCESSING
# ==============================================================================
@st.cache_data
def load_and_clean_data():
    """Load and clean the movie box office dataset for regional analysis."""
    try:
        df = pd.read_csv('movie_revenue_data.csv')
        
        if df.empty:
            st.error("❌ Dataset is empty!")
            return None
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Convert financial columns to numeric
        financial_cols = ['$Worldwide', '$Domestic', '$Foreign', 'Domestic %', 'Foreign %']
        for col in financial_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Convert other numeric columns
        df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
        df['Vote_Count'] = pd.to_numeric(df['Vote_Count'], errors='coerce')
        
        # Extract rating scores
        if 'Rating' in df.columns:
            df['Rating_Score'] = df['Rating'].str.extract(r'(\d+\.?\d*)').astype(float)
        
        # Clean genres
        if 'Genres' in df.columns:
            df['Primary_Genre'] = df['Genres'].str.split(',').str[0].str.strip()
        
        # Add regional analysis columns
        df['Worldwide_Millions'] = df['$Worldwide'] / 1_000_000
        df['Domestic_Millions'] = df['$Domestic'] / 1_000_000
        df['Foreign_Millions'] = df['$Foreign'] / 1_000_000
        df['Decade'] = (df['Year'] // 10) * 10
        
        # Regional performance indicators
        df['Domestic_Dominance'] = df['Domestic %'] > 50
        df['Foreign_Dominance'] = df['Foreign %'] > 50
        df['Regional_Balance'] = ((df['Domestic %'] - 50).abs() <= 10)
        
        # Performance categories
        df['Performance_Category'] = pd.cut(
            df['Worldwide_Millions'], 
            bins=[0, 100, 500, 1000, float('inf')],
            labels=['Low (<$100M)', 'Medium ($100M-$500M)', 'High ($500M-$1B)', 'Blockbuster (>$1B)']
        )
        
        # Regional preference ratio
        df['Domestic_Foreign_Ratio'] = df['$Domestic'] / df['$Foreign'].replace(0, 1)
        
        # Remove rows with missing critical data
        df = df.dropna(subset=['$Worldwide', 'Year'])
        
        return df
        
    except FileNotFoundError:
        st.error("❌ Dataset file 'movie_revenue_data.csv' not found!")
        return None
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None

# ==============================================================================
# VISUALIZATION FUNCTIONS
# ==============================================================================
def create_regional_comparison_chart(df, selected_movies):
    """Create regional comparison chart for selected movies"""
    movie_data = df[df['Release Group'].isin(selected_movies)].head(10)
    
    fig = go.Figure()
    
    # Domestic Revenue
    fig.add_trace(go.Bar(
        name='Domestic Revenue',
        x=movie_data['Release Group'],
        y=movie_data['Domestic_Millions'],
        marker_color='#4facfe',
        text=movie_data['Domestic_Millions'].round(1),
        textposition='auto'
    ))
    
    # Foreign Revenue
    fig.add_trace(go.Bar(
        name='Foreign Revenue',
        x=movie_data['Release Group'],
        y=movie_data['Foreign_Millions'],
        marker_color='#43e97b',
        text=movie_data['Foreign_Millions'].round(1),
        textposition='auto'
    ))
    
    fig.update_layout(
        title="Regional Box Office Comparison",
        xaxis_title="Movies",
        yaxis_title="Revenue (Millions USD)",
        barmode='group',
        template='plotly_dark',
        font=dict(family="Poppins", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_performance_scatter(df):
    """Create performance scatter plot"""
    fig = px.scatter(
        df.head(100),
        x='Domestic_Millions',
        y='Foreign_Millions',
        size='Worldwide_Millions',
        color='Primary_Genre',
        hover_data=['Release Group', 'Year'],
        title="Domestic vs Foreign Performance",
        template='plotly_dark'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins", size=12)
    )
    
    return fig

def create_genre_regional_analysis(df):
    """Create genre-wise regional analysis"""
    genre_stats = df.groupby('Primary_Genre').agg({
        'Domestic %': 'mean',
        'Foreign %': 'mean',
        'Worldwide_Millions': 'mean'
    }).round(2).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Avg Domestic %',
        x=genre_stats['Primary_Genre'],
        y=genre_stats['Domestic %'],
        marker_color='#4facfe'
    ))
    
    fig.add_trace(go.Bar(
        name='Avg Foreign %',
        x=genre_stats['Primary_Genre'],
        y=genre_stats['Foreign %'],
        marker_color='#43e97b'
    ))
    
    fig.update_layout(
        title="Genre-wise Regional Performance",
        xaxis_title="Genre",
        yaxis_title="Average Percentage",
        template='plotly_dark',
        font=dict(family="Poppins", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# ==============================================================================
# MAIN APPLICATION
# ==============================================================================

# Load dataset
df = load_and_clean_data()
if df is None:
    st.stop()

# Header
st.markdown('<h1 class="main-header">🎬 Movie Revenue Tracker</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Regional Box Office Analysis & Comparison Platform</p>', unsafe_allow_html=True)

# ==============================================================================
# SIDEBAR CONTROLS
# ==============================================================================
st.sidebar.markdown("### 🌍 Regional Analysis Controls")

all_option = "All"
min_year, max_year = int(df['Year'].min()), int(df['Year'].max())

# Year Range
year_range = st.sidebar.slider(
    "📅 Release Year Range", min_year, max_year, (min_year, max_year)
)

# Genre Filter
if 'Primary_Genre' in df.columns:
    genres = [all_option] + sorted(df['Primary_Genre'].dropna().unique())
    selected_genre = st.sidebar.selectbox("🎭 Movie Genre", genres)

# Language Filter
if 'Original_Language' in df.columns:
    languages = [all_option] + sorted(df['Original_Language'].dropna().unique())
    selected_language = st.sidebar.selectbox("🗣️ Original Language", languages)

# Regional Performance Filter
regional_filter = st.sidebar.selectbox(
    "🌍 Regional Performance Focus",
    [all_option, "Domestic Dominance (>50%)", "Foreign Dominance (>50%)", "Balanced Performance"]
)

# Revenue Range
revenue_range = st.sidebar.slider(
    "💰 Worldwide Revenue Range (M USD)",
    float(df['Worldwide_Millions'].min()),
    float(df['Worldwide_Millions'].max()),
    (float(df['Worldwide_Millions'].min()), float(df['Worldwide_Millions'].max()))
)

# Display Options
st.sidebar.markdown("### 📊 Display Options")
show_top_n = st.sidebar.number_input("🔢 Show Top N Movies", 5, 50, 15)
analysis_type = st.sidebar.radio(
    "🔍 Analysis Focus",
    ["Regional Comparison", "Revenue Performance", "Genre Analysis", "Market Trends"]
)

# ==============================================================================
# FILTER DATA
# ==============================================================================
filtered_df = df.copy()

# Apply filters
filtered_df = filtered_df[
    (filtered_df['Year'] >= year_range[0]) & 
    (filtered_df['Year'] <= year_range[1])
]

if selected_genre != all_option:
    filtered_df = filtered_df[filtered_df['Primary_Genre'] == selected_genre]

if 'selected_language' in locals() and selected_language != all_option:
    filtered_df = filtered_df[filtered_df['Original_Language'] == selected_language]

if regional_filter == "Domestic Dominance (>50%)":
    filtered_df = filtered_df[filtered_df['Domestic_Dominance'] == True]
elif regional_filter == "Foreign Dominance (>50%)":
    filtered_df = filtered_df[filtered_df['Foreign_Dominance'] == True]
elif regional_filter == "Balanced Performance":
    filtered_df = filtered_df[filtered_df['Regional_Balance'] == True]

filtered_df = filtered_df[
    (filtered_df['Worldwide_Millions'] >= revenue_range[0]) & 
    (filtered_df['Worldwide_Millions'] <= revenue_range[1])
]

# ==============================================================================
# KEY METRICS
# ==============================================================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>🎬</h3>
        <h2>{len(filtered_df):,}</h2>
        <p>Total Movies</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    avg_worldwide = filtered_df['Worldwide_Millions'].mean()
    st.markdown(f"""
    <div class="metric-card">
        <h3>💰</h3>
        <h2>${avg_worldwide:.1f}M</h2>
        <p>Avg Worldwide</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    avg_domestic_pct = filtered_df['Domestic %'].mean()
    st.markdown(f"""
    <div class="metric-card">
        <h3>🇺🇸</h3>
        <h2>{avg_domestic_pct:.1f}%</h2>
        <p>Avg Domestic</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    avg_foreign_pct = filtered_df['Foreign %'].mean()
    st.markdown(f"""
    <div class="metric-card">
        <h3>🌍</h3>
        <h2>{avg_foreign_pct:.1f}%</h2>
        <p>Avg Foreign</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# ANALYSIS TABS
# ==============================================================================
tab1, tab2, tab3, tab4 = st.tabs(["🌍 Regional Comparison", "📊 Revenue Performance", "🎭 Genre Analysis", "📈 Market Trends"])

with tab1:
    st.markdown('<h2 class="analysis-header">Regional Box Office Comparison</h2>', unsafe_allow_html=True)
    
    # Top movies for comparison
    top_movies = filtered_df.nlargest(show_top_n, 'Worldwide_Millions')['Release Group'].tolist()
    selected_movies = st.multiselect(
        "Select Movies for Comparison",
        options=top_movies,
        default=top_movies[:5]
    )
    
    if selected_movies:
        fig = create_regional_comparison_chart(filtered_df, selected_movies)
        st.plotly_chart(fig, use_container_width=True)
        
        # Regional performance table
        st.subheader("📋 Regional Performance Details")
        comparison_data = filtered_df[filtered_df['Release Group'].isin(selected_movies)][
            ['Release Group', 'Worldwide_Millions', 'Domestic_Millions', 'Foreign_Millions', 'Domestic %', 'Foreign %']
        ].round(2)
        st.dataframe(comparison_data, use_container_width=True)

with tab2:
    st.markdown('<h2 class="analysis-header">Revenue Performance Analysis</h2>', unsafe_allow_html=True)
    
    # Performance scatter plot
    fig = create_performance_scatter(filtered_df)
    st.plotly_chart(fig, use_container_width=True)
    
    # Top performers by category
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top Domestic Performers")
        top_domestic = filtered_df.nlargest(10, 'Domestic_Millions')[
            ['Release Group', 'Domestic_Millions', 'Domestic %']
        ].round(2)
        st.dataframe(top_domestic, use_container_width=True)
    
    with col2:
        st.subheader("🌍 Top Foreign Performers")
        top_foreign = filtered_df.nlargest(10, 'Foreign_Millions')[
            ['Release Group', 'Foreign_Millions', 'Foreign %']
        ].round(2)
        st.dataframe(top_foreign, use_container_width=True)

with tab3:
    st.markdown('<h2 class="analysis-header">Genre-wise Regional Analysis</h2>', unsafe_allow_html=True)
    
    # Genre regional analysis chart
    if 'Primary_Genre' in filtered_df.columns:
        fig = create_genre_regional_analysis(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
        
        # Genre statistics table
        st.subheader("📊 Genre Statistics")
        genre_stats = filtered_df.groupby('Primary_Genre').agg({
            'Worldwide_Millions': ['count', 'mean', 'sum'],
            'Domestic %': 'mean',
            'Foreign %': 'mean'
        }).round(2)
        genre_stats.columns = ['Count', 'Avg Revenue (M)', 'Total Revenue (M)', 'Avg Domestic %', 'Avg Foreign %']
        st.dataframe(genre_stats, use_container_width=True)

with tab4:
    st.markdown('<h2 class="analysis-header">Market Trends Analysis</h2>', unsafe_allow_html=True)
    
    # Yearly trends
    yearly_trends = filtered_df.groupby('Year').agg({
        'Worldwide_Millions': 'mean',
        'Domestic %': 'mean',
        'Foreign %': 'mean'
    }).reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=yearly_trends['Year'],
        y=yearly_trends['Domestic %'],
        mode='lines+markers',
        name='Domestic %',
        line=dict(color='#4facfe', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=yearly_trends['Year'],
        y=yearly_trends['Foreign %'],
        mode='lines+markers',
        name='Foreign %',
        line=dict(color='#43e97b', width=3)
    ))
    
    fig.update_layout(
        title="Regional Market Share Trends Over Time",
        xaxis_title="Year",
        yaxis_title="Average Percentage",
        template='plotly_dark',
        font=dict(family="Poppins", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Decade analysis
    st.subheader("📅 Decade-wise Performance")
    decade_stats = filtered_df.groupby('Decade').agg({
        'Worldwide_Millions': ['count', 'mean'],
        'Domestic %': 'mean',
        'Foreign %': 'mean'
    }).round(2)
    decade_stats.columns = ['Movie Count', 'Avg Revenue (M)', 'Avg Domestic %', 'Avg Foreign %']
    st.dataframe(decade_stats, use_container_width=True)

# ==============================================================================
# FOOTER
# ==============================================================================
st.markdown("""
<div class="footer">
    <p>🎬 Movie Revenue Tracker - Regional Analysis Platform</p>
    <p>Powered by Streamlit & Plotly | Data-driven Box Office Insights</p>
</div>
""", unsafe_allow_html=True)
