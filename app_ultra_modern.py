import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from typing import Dict, List, Tuple, Optional
import warnings
import time
import uuid
warnings.filterwarnings('ignore')

# Import our modular components
from src.config.settings import AppConfig, ChartConfig, ColorScheme
from src.styles.ultra_modern_theme import load_ultra_modern_theme
from src.data.processor import DataProcessor
from src.visualizations.charts import ChartCreator
from src.components.ui_elements import UIComponents

class UltraModernMovieTracker:
    """Ultra-Modern Movie Revenue Tracker with Cinematic Interface"""
    
    def __init__(self):
        """Initialize the ultra-modern movie tracker"""
        self.config = AppConfig()
        self.chart_config = ChartConfig()
        self.colors = ColorScheme()
        
        # Generate unique session ID for widgets
        if 'session_id' not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())[:8]
        self.session_id = st.session_state.session_id
        
        # Initialize components
        self.data_processor = DataProcessor()
        self.chart_creator = ChartCreator()
        self.ui = UIComponents()
        
        # Load data
        self.data = self.data_processor.load_data()
        
    def setup_page_config(self):
        """Configure Streamlit page with ultra-modern settings"""
        st.set_page_config(
            page_title="🎬 Movie Revenue Tracker - Ultra Modern",
            page_icon="🎬",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                'Get Help': 'https://github.com/yourusername/movie-revenue-tracker',
                'Report a bug': 'https://github.com/yourusername/movie-revenue-tracker/issues',
                'About': "Ultra-Modern Movie Revenue Analytics Platform"
            }
        )
        
    def load_custom_styles(self):
        """Load ultra-modern cinematic theme"""
        st.markdown(load_ultra_modern_theme(), unsafe_allow_html=True)
        
    def render_hero_section(self):
        """Render cinematic hero section"""
        st.markdown("""
        <div class="main-header">
            🎬 MOVIE REVENUE TRACKER
        </div>
        <div class="sub-header">
            Experience the Future of Box Office Analytics
        </div>
        """, unsafe_allow_html=True)
        
    def render_key_metrics(self, filtered_data: pd.DataFrame):
        """Render animated key metrics cards"""
        st.markdown("""
        <div class="analysis-header">
            📊 PERFORMANCE METRICS
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_revenue = filtered_data['$Worldwide'].sum() / 1_000_000
        avg_revenue = filtered_data['$Worldwide'].mean() / 1_000_000
        total_movies = len(filtered_data)
        top_movie = filtered_data.loc[filtered_data['$Worldwide'].idxmax(), 'Release Group'] if not filtered_data.empty else "N/A"
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>💰</h3>
                <h2>${total_revenue:,.0f}M</h2>
                <p>Total Revenue</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>📈</h3>
                <h2>${avg_revenue:,.0f}M</h2>
                <p>Average Revenue</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🎬</h3>
                <h2>{total_movies}</h2>
                <p>Total Movies</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🏆</h3>
                <h2 style="font-size: 1.2rem;">{top_movie[:20]}{'...' if len(top_movie) > 20 else ''}</h2>
                <p>Top Performer</p>
            </div>
            """, unsafe_allow_html=True)
            
    def render_sidebar_controls(self) -> Tuple[List[str], List[str], Tuple[float, float]]:
        """Render ultra-modern sidebar controls"""
        st.sidebar.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 class="text-gradient">🎛️ CONTROL PANEL</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Movie selection with ultra-modern styling
        st.sidebar.markdown("### 🎬 Movie Selection")
        movies = ['All Movies'] + sorted(self.data['Release Group'].unique().tolist())
        selected_movies = st.sidebar.multiselect(
            "Choose movies to analyze:",
            movies,
            default=['All Movies'],
            help="Select specific movies or keep 'All Movies' for complete analysis",
            key=f"movie_selector_{self.session_id}"
        )
        
        # Region selection
        st.sidebar.markdown("### 🌍 Regional Analysis")
        regions = ['All Regions'] + [col for col in self.data.columns if col not in ['Release Group', '$Worldwide', 'Rank']]
        selected_regions = st.sidebar.multiselect(
            "Select regions to compare:",
            regions,
            default=['All Regions'],
            help="Choose regions for comparative analysis",
            key=f"region_selector_{self.session_id}"
        )
        
        # Revenue filter
        st.sidebar.markdown("### 💰 Revenue Filter")
        min_revenue = float(self.data['$Worldwide'].min() / 1_000_000)
        max_revenue = float(self.data['$Worldwide'].max() / 1_000_000)
        revenue_range = st.sidebar.slider(
            "Revenue range (in millions):",
            min_value=min_revenue,
            max_value=max_revenue,
            value=(min_revenue, max_revenue),
            step=10.0,
            help="Filter movies by worldwide revenue",
            key=f"revenue_slider_{self.session_id}"
        )
        
        # Advanced options
        with st.sidebar.expander("🔧 Advanced Options", expanded=False):
            st.markdown("### 📊 Chart Options")
            show_animations = st.checkbox("Enable animations", value=True, key="animations_checkbox")
            show_hover_data = st.checkbox("Show detailed hover info", value=True, key="hover_checkbox")
            
            st.markdown("### 🎨 Display Options")
            chart_height = st.slider("Chart height", 400, 800, 500, key="chart_height_slider")
            
        return selected_movies, selected_regions, revenue_range
    
    def filter_data_simple(self, selected_movies: List[str], 
                          selected_regions: List[str], revenue_range: Tuple[float, float]) -> pd.DataFrame:
        """
        Filter data based on user selections
        
        Args:
            selected_movies: List of selected movie titles
            selected_regions: List of selected regions
            revenue_range: Tuple of (min_revenue, max_revenue)
            
        Returns:
            pd.DataFrame: Filtered dataframe
        """
        filtered_data = self.data.copy()
        
        # Filter by movies
        if 'All Movies' not in selected_movies and selected_movies:
            filtered_data = filtered_data[filtered_data['Release Group'].isin(selected_movies)]
        
        # Filter by revenue range (converting to millions for comparison)
        min_revenue, max_revenue = revenue_range
        revenue_millions = filtered_data['$Worldwide'] / 1_000_000
        filtered_data = filtered_data[
            (revenue_millions >= min_revenue) & 
            (revenue_millions <= max_revenue)
        ]
        
        return filtered_data
        
    def render_analysis_tabs(self, filtered_data: pd.DataFrame, selected_regions: List[str]):
        """Render analysis tabs with ultra-modern styling"""
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Revenue Analysis", 
            "🌍 Regional Comparison", 
            "📈 Performance Insights",
            "📋 Data Explorer"
        ])
        
        with tab1:
            self.render_revenue_analysis(filtered_data, selected_regions)
            
        with tab2:
            self.render_regional_comparison(filtered_data, selected_regions)
            
        with tab3:
            self.render_performance_insights(filtered_data)
            
        with tab4:
            self.render_data_explorer(filtered_data)
            
    def render_revenue_analysis(self, filtered_data: pd.DataFrame, selected_regions: List[str]):
        """Render revenue analysis with ultra-modern charts"""
        st.markdown("""
        <div class="content-card">
            <h2 class="text-gradient">💰 Revenue Performance Analysis</h2>
            <p>Comprehensive analysis of box office performance across movies and regions.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Top movies bar chart
            top_movies = filtered_data.nlargest(10, '$Worldwide')
            fig_bar = self.chart_creator.create_bar_chart(
                top_movies,
                x='Release Group',
                y='$Worldwide',
                title="🏆 Top 10 Movies by Worldwide Revenue",
                color_column='$Worldwide'
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
        with col2:
            # Revenue distribution pie chart
            if len(filtered_data) > 0:
                # Create revenue categories
                revenue_millions = filtered_data['$Worldwide'] / 1_000_000
                filtered_data['Revenue_Category'] = pd.cut(
                    revenue_millions,
                    bins=[0, 100, 300, 500, 1000, float('inf')],
                    labels=['<$100M', '$100M-$300M', '$300M-$500M', '$500M-$1B', '$1B+']
                )
                
                category_counts = filtered_data['Revenue_Category'].value_counts()
                
                fig_pie = self.chart_creator.create_pie_chart(
                    category_counts.values,
                    category_counts.index,
                    title="💼 Revenue Distribution"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
                
    def render_regional_comparison(self, filtered_data: pd.DataFrame, selected_regions: List[str]):
        """Render regional comparison analysis"""
        st.markdown("""
        <div class="content-card">
            <h2 class="text-gradient">🌍 Regional Market Analysis</h2>
            <p>Compare box office performance across different global markets.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if 'All Regions' not in selected_regions and len(selected_regions) > 0:
            regions_to_plot = selected_regions
        else:
            regions_to_plot = [col for col in filtered_data.columns if col not in ['Release Group', '$Worldwide', 'Rank']]
            
        if len(regions_to_plot) > 0:
            # Regional performance heatmap
            regional_data = filtered_data[['Release Group'] + regions_to_plot].set_index('Release Group')
            
            # Get top 15 movies for better visualization
            top_movies_regional = filtered_data.nlargest(15, '$Worldwide')['Release Group'].tolist()
            regional_data_top = regional_data.loc[top_movies_regional]
            
            fig_heatmap = self.chart_creator.create_heatmap(
                regional_data_top,
                title="🔥 Regional Performance Heatmap - Top Movies"
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
            
            # Regional comparison scatter plot
            col1, col2 = st.columns(2)
            
            with col1:
                if len(regions_to_plot) >= 2:
                    fig_scatter = self.chart_creator.create_scatter_plot(
                        filtered_data,
                        x=regions_to_plot[0],
                        y=regions_to_plot[1] if len(regions_to_plot) > 1 else regions_to_plot[0],
                        title=f"📈 {regions_to_plot[0]} vs {regions_to_plot[1] if len(regions_to_plot) > 1 else regions_to_plot[0]}",
                        hover_data=['Release Group']
                    )
                    st.plotly_chart(fig_scatter, use_container_width=True)
                    
            with col2:
                # Regional market share
                regional_totals = filtered_data[regions_to_plot].sum()
                fig_regional_pie = self.chart_creator.create_pie_chart(
                    regional_totals.values,
                    regional_totals.index,
                    title="🥧 Regional Market Share"
                )
                st.plotly_chart(fig_regional_pie, use_container_width=True)
                
    def render_performance_insights(self, filtered_data: pd.DataFrame):
        """Render performance insights and analytics"""
        st.markdown("""
        <div class="content-card">
            <h2 class="text-gradient">📈 Advanced Performance Insights</h2>
            <p>Deep dive into performance patterns and statistical analysis.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Performance distribution
            fig_dist = go.Figure()
            fig_dist.add_trace(go.Histogram(
                x=filtered_data['$Worldwide'] / 1_000_000,
                nbinsx=20,
                name="Worldwide Revenue",
                marker_color=self.colors.NEON_CYAN,
                opacity=0.7
            ))
            
            fig_dist.update_layout(
                title="📊 Revenue Distribution Analysis",
                xaxis_title="Revenue (Millions USD)",
                yaxis_title="Number of Movies",
                template="plotly_dark",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', family='Inter'),
                showlegend=False
            )
            
            st.plotly_chart(fig_dist, use_container_width=True)
            
        with col2:
            # Box plot for regional analysis
            regions = [col for col in filtered_data.columns if col not in ['Release Group', '$Worldwide', 'Rank']]
            if len(regions) > 0:
                fig_box = go.Figure()
                
                for i, region in enumerate(regions[:5]):  # Limit to 5 regions for clarity
                    if region in filtered_data.columns:
                        fig_box.add_trace(go.Box(
                            y=filtered_data[region] / 1_000_000 if filtered_data[region].dtype in ['int64', 'float64'] else filtered_data[region],
                            name=region,
                            marker_color=self.colors.get_color_by_index(i),
                            boxpoints='outliers'
                        ))
                
                fig_box.update_layout(
                    title="📦 Regional Revenue Distribution",
                    yaxis_title="Revenue (Millions USD)",
                    template="plotly_dark",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white', family='Inter')
                )
                
                st.plotly_chart(fig_box, use_container_width=True)
                
        # Performance statistics
        st.markdown("### 📊 Statistical Summary")
        revenue_millions = filtered_data['$Worldwide'] / 1_000_000
        stats_data = {
            'Metric': ['Mean Revenue', 'Median Revenue', 'Standard Deviation', 'Min Revenue', 'Max Revenue'],
            'Worldwide ($M)': [
                f"${revenue_millions.mean():,.0f}",
                f"${revenue_millions.median():,.0f}",
                f"${revenue_millions.std():,.0f}",
                f"${revenue_millions.min():,.0f}",
                f"${revenue_millions.max():,.0f}"
            ]
        }
        
        stats_df = pd.DataFrame(stats_data)
        st.dataframe(stats_df, use_container_width=True, hide_index=True)
        
    def render_data_explorer(self, filtered_data: pd.DataFrame):
        """Render interactive data explorer"""
        st.markdown("""
        <div class="content-card">
            <h2 class="text-gradient">📋 Interactive Data Explorer</h2>
            <p>Explore the complete dataset with sorting and filtering capabilities.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Data summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Records", len(filtered_data))
        with col2:
            st.metric("Total Columns", len(filtered_data.columns))
        with col3:
            total_revenue = filtered_data['$Worldwide'].sum() / 1_000_000
            st.metric("Total Revenue", f"${total_revenue:,.0f}M")
            
        # Search and filter options
        search_term = st.text_input("🔍 Search movies:", placeholder="Enter movie title...", key="movie_search")
        
        if search_term:
            mask = filtered_data['Release Group'].str.contains(search_term, case=False, na=False)
            display_data = filtered_data[mask]
        else:
            display_data = filtered_data
            
        # Sorting options
        col1, col2 = st.columns(2)
        with col1:
            sort_column = st.selectbox("Sort by:", filtered_data.columns, key="sort_column_select")
        with col2:
            sort_ascending = st.selectbox("Order:", ["Descending", "Ascending"], key="sort_order_select") == "Ascending"
            
        # Apply sorting
        display_data = display_data.sort_values(sort_column, ascending=sort_ascending)
        
        # Display data with enhanced styling
        st.markdown("### 📊 Data Table")
        
        # Format numerical columns
        numeric_columns = display_data.select_dtypes(include=[np.number]).columns
        formatted_data = display_data.copy()
        
        for col in numeric_columns:
            if col not in ['Release Group', 'Rank', 'Year', 'Vote_Count']:
                if '$' in col or 'revenue' in col.lower():
                    formatted_data[col] = formatted_data[col].apply(lambda x: f"${x/1_000_000:,.0f}M" if pd.notna(x) else "N/A")
                elif '%' in col:
                    formatted_data[col] = formatted_data[col].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")
                else:
                    formatted_data[col] = formatted_data[col].apply(lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A")
        
        st.dataframe(
            formatted_data,
            use_container_width=True,
            hide_index=True,
            height=400
        )
        
        # Download options
        st.markdown("### 📥 Export Data")
        col1, col2 = st.columns(2)
        
        with col1:
            csv = display_data.to_csv(index=False)
            st.download_button(
                "📄 Download as CSV",
                csv,
                "movie_revenue_data.csv",
                "text/csv",
                key='download-csv-ultra'
            )
            
        with col2:
            # Convert to Excel
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                display_data.to_excel(writer, sheet_name='Movie Revenue Data', index=False)
            excel_data = output.getvalue()
            
            st.download_button(
                "📊 Download as Excel",
                excel_data,
                "movie_revenue_data.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key='download-excel-ultra'
            )
            
    def run(self):
        """Run the ultra-modern movie tracker application"""
        # Setup page configuration
        self.setup_page_config()
        
        # Load ultra-modern theme
        self.load_custom_styles()
        
        # Render hero section
        self.render_hero_section()
        
        # Render sidebar controls
        selected_movies, selected_regions, revenue_range = self.render_sidebar_controls()
        
        # Render sidebar controls
        selected_movies, selected_regions, revenue_range = self.render_sidebar_controls()
        
        # Filter data based on selections
        filtered_data = self.filter_data_simple(selected_movies, selected_regions, revenue_range)
        
        if filtered_data.empty:
            st.warning("⚠️ No data matches your current filters. Please adjust your selection.")
            return
            
        # Render key metrics
        self.render_key_metrics(filtered_data)
        
        # Render analysis tabs
        self.render_analysis_tabs(filtered_data, selected_regions)
        
        # Footer
        st.markdown("""
        <div style="text-align: center; margin-top: 3rem; padding: 2rem; opacity: 0.7;">
            <p class="text-gradient">🎬 Movie Revenue Tracker - Ultra Modern Edition</p>
            <p>Built with ❤️ using Streamlit, Plotly, and cutting-edge design</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application entry point"""
    app = UltraModernMovieTracker()
    app.run()

if __name__ == "__main__":
    main()
