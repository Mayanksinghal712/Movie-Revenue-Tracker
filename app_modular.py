import streamlit as st
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.config.settings import configure_page
from src.styles.dark_mode import load_dark_mode_css
from src.data.processor import DataProcessor
from src.visualizations.charts import ChartCreator
from src.components.ui_elements import UIComponents

# ==============================================================================
# MAIN APPLICATION CLASS
# ==============================================================================
class MovieRevenueTracker:
    """Main application class for Movie Revenue Tracker"""
    
    def __init__(self):
        """Initialize the application"""
        configure_page()
        self.load_styles()
        self.data_processor = DataProcessor()
        self.chart_creator = ChartCreator()
        self.ui = UIComponents()
        
    def load_styles(self):
        """Load custom CSS styles"""
        st.markdown(load_dark_mode_css(), unsafe_allow_html=True)
    
    def run(self):
        """Run the main application"""
        # Load and process data
        df = self.data_processor.load_and_clean_data()
        
        if df is None:
            self.ui.create_error_message("Failed to load data. Please check if 'movie_revenue_data.csv' exists.")
            return
        
        # Create header
        self.ui.create_header(
            "🎬 Movie Revenue Tracker",
            "🌍 Regional Box Office Performance & Collection Analysis Platform 📊"
        )
        
        # Create sidebar filters
        filters = self.ui.create_sidebar_filters(df)
        
        # Apply filters to data
        filtered_df = self.data_processor.apply_filters(
            df,
            filters['year_range'],
            filters['selected_genre'],
            filters['selected_language'], 
            filters['regional_filter'],
            filters['revenue_range']
        )
        
        # Check if filtered data is empty
        if filtered_df.empty:
            self.ui.create_warning_message("No data matches the selected filters. Please adjust your filter criteria.")
            return
        
        # Get summary statistics
        stats = self.data_processor.get_summary_stats(filtered_df)
        
        # Create metrics display
        self.ui.create_extended_metrics_row(stats)
        
        # Create filter summary
        self.ui.create_filter_summary(filters)
        
        st.markdown("---")
        
        # Main analysis content based on selected type
        self.render_analysis_content(filtered_df, filters)
        
        # Create footer
        self.ui.create_footer()
    
    def render_analysis_content(self, df, filters):
        """
        Render the main analysis content based on selected analysis type
        
        Args:
            df: Filtered dataframe
            filters: Applied filters
        """
        analysis_type = filters['analysis_type']
        
        if analysis_type == "Regional Comparison":
            self.render_regional_comparison(df, filters)
        elif analysis_type == "Revenue Performance":
            self.render_revenue_performance(df, filters)
        elif analysis_type == "Genre Analysis":
            self.render_genre_analysis(df, filters)
        elif analysis_type == "Market Trends":
            self.render_market_trends(df, filters)
        elif analysis_type == "🎨 Advanced Visualizations":
            self.render_advanced_visualizations(df, filters)
    
    def render_regional_comparison(self, df, filters):
        """Render regional comparison analysis"""
        self.ui.create_analysis_header("🌍 Cross-Regional Box Office Comparison")
        
        tab1, tab2, tab3 = st.tabs(["📊 Movie Comparison", "🌐 Regional Breakdown", "📈 Trends Analysis"])
        
        with tab1:
            # Movie selection and comparison
            selected_movies = self.ui.create_movie_selector(df, filters['show_top_n'])
            
            if selected_movies:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Regional comparison chart
                    fig1 = self.chart_creator.create_regional_comparison_chart(df, selected_movies)
                    st.plotly_chart(fig1, use_container_width=True)
                
                with col2:
                    # Performance scatter plot
                    fig2 = self.chart_creator.create_performance_scatter(df)
                    st.plotly_chart(fig2, use_container_width=True)
                
                # Regional performance details table
                self.ui.create_data_table(
                    df[df['Release Group'].isin(selected_movies)][
                        ['Release Group', 'Worldwide_Millions', 'Domestic_Millions', 
                         'Foreign_Millions', 'Domestic %', 'Foreign %']
                    ].round(2),
                    "📋 Regional Performance Details"
                )
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Regional dominance distribution
                dominance_data = {
                    'Domestic Dominance': len(df[df['Domestic_Dominance']]),
                    'Foreign Dominance': len(df[df['Foreign_Dominance']]),
                    'Balanced Performance': len(df[df['Regional_Balance']])
                }
                fig3 = self.chart_creator.create_pie_chart(dominance_data, "Regional Performance Distribution")
                st.plotly_chart(fig3, use_container_width=True)
            
            with col2:
                # Top performers by region
                top_domestic = self.data_processor.get_top_performers(df, 10, 'domestic')
                self.ui.create_data_table(
                    top_domestic[['Release Group', 'Domestic_Millions', 'Domestic %']].round(2),
                    "🏆 Top Domestic Performers"
                )
        
        with tab3:
            # Revenue trends over time
            fig4 = self.chart_creator.create_revenue_trends_chart(df)
            st.plotly_chart(fig4, use_container_width=True)
            
            # Yearly analysis table
            yearly_trends = self.data_processor.get_yearly_trends(df)
            self.ui.create_data_table(yearly_trends, "📅 Yearly Trends Summary")
    
    def render_revenue_performance(self, df, filters):
        """Render revenue performance analysis"""
        self.ui.create_analysis_header("📊 Revenue Performance Analysis")
        
        tab1, tab2 = st.tabs(["🏆 Top Performers", "📈 Performance Metrics"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Top movies chart
                fig1 = self.chart_creator.create_top_performers_chart(df, filters['show_top_n'])
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # Performance categories distribution
                if 'Performance_Category' in df.columns:
                    category_counts = df['Performance_Category'].value_counts().to_dict()
                    fig2 = self.chart_creator.create_pie_chart(category_counts, "Performance Categories")
                    st.plotly_chart(fig2, use_container_width=True)
        
        with tab2:
            # Performance scatter plot
            fig3 = self.chart_creator.create_performance_scatter(df)
            st.plotly_chart(fig3, use_container_width=True)
            
            # Performance statistics
            col1, col2 = st.columns(2)
            
            with col1:
                top_worldwide = self.data_processor.get_top_performers(df, 10, 'worldwide')
                self.ui.create_data_table(
                    top_worldwide[['Release Group', 'Worldwide_Millions', 'Year']].round(2),
                    "🌍 Top Worldwide Earners"
                )
            
            with col2:
                top_foreign = self.data_processor.get_top_performers(df, 10, 'foreign')
                self.ui.create_data_table(
                    top_foreign[['Release Group', 'Foreign_Millions', 'Foreign %']].round(2),
                    "🌎 Top Foreign Earners"
                )
    
    def render_genre_analysis(self, df, filters):
        """Render genre analysis"""
        self.ui.create_analysis_header("🎭 Genre-wise Regional Analysis")
        
        if 'Primary_Genre' not in df.columns:
            self.ui.create_warning_message("Genre data not available for analysis")
            return
        
        # Genre regional performance chart
        fig1 = self.chart_creator.create_genre_regional_analysis(df)
        st.plotly_chart(fig1, use_container_width=True)
        
        # Genre statistics table
        genre_stats = self.data_processor.get_genre_analysis(df)
        self.ui.create_data_table(genre_stats, "📊 Genre Performance Statistics")
        
        # Genre insights
        if not genre_stats.empty:
            best_domestic_genre = genre_stats.loc[genre_stats['Avg_Domestic_Pct'].idxmax(), 'Primary_Genre']
            best_foreign_genre = genre_stats.loc[genre_stats['Avg_Foreign_Pct'].idxmax(), 'Primary_Genre']
            highest_revenue_genre = genre_stats.loc[genre_stats['Total_Revenue_M'].idxmax(), 'Primary_Genre']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                self.ui.create_info_box(
                    "Best Domestic Genre",
                    f"{best_domestic_genre} performs best in domestic markets",
                    "success"
                )
            
            with col2:
                self.ui.create_info_box(
                    "Best Foreign Genre", 
                    f"{best_foreign_genre} dominates foreign markets",
                    "info"
                )
            
            with col3:
                self.ui.create_info_box(
                    "Highest Revenue Genre",
                    f"{highest_revenue_genre} generates the most total revenue",
                    "warning"
                )
    
    def render_market_trends(self, df, filters):
        """Render market trends analysis"""
        self.ui.create_analysis_header("📈 Market Trends Analysis")
        
        # Revenue trends over time
        fig1 = self.chart_creator.create_revenue_trends_chart(df)
        st.plotly_chart(fig1, use_container_width=True)
        
        # Decade analysis
        if 'Decade' in df.columns:
            decade_stats = df.groupby('Decade').agg({
                'Worldwide_Millions': ['count', 'mean'],
                'Domestic %': 'mean',
                'Foreign %': 'mean'
            }).round(2)
            decade_stats.columns = ['Movie Count', 'Avg Revenue (M)', 'Avg Domestic %', 'Avg Foreign %']
            
            self.ui.create_data_table(decade_stats.reset_index(), "📅 Decade-wise Performance")
        
        # Market insights
        current_year = df['Year'].max()
        recent_data = df[df['Year'] >= current_year - 5]
        
        if not recent_data.empty:
            avg_domestic_recent = recent_data['Domestic %'].mean()
            avg_foreign_recent = recent_data['Foreign %'].mean()
            
            col1, col2 = st.columns(2)
            
            with col1:
                trend_direction = "increasing" if avg_foreign_recent > 50 else "decreasing"
                self.ui.create_info_box(
                    "Recent Market Trend",
                    f"Foreign market share is {trend_direction} ({avg_foreign_recent:.1f}% in recent years)",
                    "info"
                )
            
            with col2:
                growth_movies = len(recent_data[recent_data['Worldwide_Millions'] > 500])
                self.ui.create_info_box(
                    "High-Grossing Movies",
                    f"{growth_movies} movies grossed over $500M in recent years",
                    "success"
                )
    
    def render_advanced_visualizations(self, df, filters):
        """Render advanced and beautiful visualizations"""
        self.ui.create_analysis_header("🎨 Advanced Data Visualizations")
        
        st.markdown("""
        <div class="glass-card">
            <h3>🌟 Explore stunning advanced charts and interactive visualizations</h3>
            <p>Experience next-generation data visualization with 3D plots, animations, and beautiful designs.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create tabs for different visualization types
        tab1, tab2, tab3, tab4 = st.tabs([
            "🌌 3D Universe", "🎭 Animated Timeline", "🌟 Radial Charts", "💎 Special Effects"
        ])
        
        with tab1:
            st.markdown("### 🌌 3D Movie Performance Universe")
            st.markdown("*Navigate through a 3D space where each bubble represents a movie*")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                fig_3d = self.chart_creator.create_advanced_3d_scatter(df)
                st.plotly_chart(fig_3d, use_container_width=True)
            
            with col2:
                st.markdown("""
                **🎯 How to explore:**
                - 🖱️ **Rotate**: Click and drag to spin the view
                - 🔍 **Zoom**: Scroll to zoom in/out
                - 👆 **Hover**: See movie details
                - 🎨 **Colors**: Different genres
                - 📏 **Size**: Bubble size = Total revenue
                """)
        
        with tab2:
            st.markdown("### 🎭 Animated Genre Evolution Timeline")
            st.markdown("*Watch how different movie genres evolved over the years*")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                fig_animated = self.chart_creator.create_animated_timeline_chart(df)
                st.plotly_chart(fig_animated, use_container_width=True)
            
            with col2:
                st.markdown("""
                **🎮 Animation Controls:**
                - ▶️ **Play**: Watch the timeline unfold
                - ⏸️ **Pause**: Stop at any year
                - 🔄 **Loop**: Continuous playback
                - 📊 **Observe**: Genre movements over time
                - 💫 **Bubbles**: Larger = Higher revenue
                """)
        
        with tab3:
            st.markdown("### 🌟 Radial Performance Charts")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🌟 Genre Performance Radar")
                fig_radial = self.chart_creator.create_radial_chart(df)
                st.plotly_chart(fig_radial, use_container_width=True)
            
            with col2:
                st.markdown("#### ☀️ Revenue Sunburst")
                fig_sunburst = self.chart_creator.create_sunburst_chart(df)
                st.plotly_chart(fig_sunburst, use_container_width=True)
        
        with tab4:
            st.markdown("### 💎 Special Effect Visualizations")
            
            # Create sub-tabs for different special effects
            subtab1, subtab2, subtab3, subtab4 = st.tabs([
                "💰 Waterfall", "🔥 Heatmap", "🎻 Violin Plot", "📊 All Charts"
            ])
            
            with subtab1:
                st.markdown("#### 💰 Revenue Waterfall Analysis")
                if 'Release Group' in df.columns:
                    selected_movie = st.selectbox(
                        "Choose a movie for waterfall analysis:",
                        df['Release Group'].head(20).tolist(),
                        key="waterfall_movie"
                    )
                    
                    if selected_movie:
                        fig_waterfall = self.chart_creator.create_waterfall_chart(df, selected_movie)
                        st.plotly_chart(fig_waterfall, use_container_width=True)
                else:
                    st.info("Movie data not available for waterfall analysis")
            
            with subtab2:
                st.markdown("#### 🔥 Correlation Heatmap")
                fig_heatmap = self.chart_creator.create_heatmap_correlation(df)
                st.plotly_chart(fig_heatmap, use_container_width=True)
            
            with subtab3:
                st.markdown("#### 🎻 Revenue Distribution Violin Plot")
                fig_violin = self.chart_creator.create_violin_plot(df)
                st.plotly_chart(fig_violin, use_container_width=True)
            
            with subtab4:
                st.markdown("#### 📊 Chart Gallery Overview")
                
                # Create a grid of smaller charts
                col1, col2 = st.columns(2)
                
                with col1:
                    # Mini radial chart
                    fig_mini_radial = self.chart_creator.create_radial_chart(df)
                    fig_mini_radial.update_layout(height=300)
                    st.plotly_chart(fig_mini_radial, use_container_width=True)
                    
                    # Mini heatmap
                    fig_mini_heatmap = self.chart_creator.create_heatmap_correlation(df)
                    fig_mini_heatmap.update_layout(height=300)
                    st.plotly_chart(fig_mini_heatmap, use_container_width=True)
                
                with col2:
                    # Mini violin plot
                    fig_mini_violin = self.chart_creator.create_violin_plot(df)
                    fig_mini_violin.update_layout(height=300)
                    st.plotly_chart(fig_mini_violin, use_container_width=True)
                    
                    # Mini sunburst
                    fig_mini_sunburst = self.chart_creator.create_sunburst_chart(df)
                    fig_mini_sunburst.update_layout(height=300)
                    st.plotly_chart(fig_mini_sunburst, use_container_width=True)
        
        # Add usage tips
        st.markdown("---")
        st.markdown("""
        <div class="glass-card">
            <h4>💡 Pro Tips for Advanced Visualizations:</h4>
            <ul>
                <li>🖱️ <strong>Interactive Elements</strong>: All charts support hover, zoom, and pan</li>
                <li>🎨 <strong>Color Coding</strong>: Different colors represent different genres or categories</li>
                <li>📊 <strong>Size Matters</strong>: Bubble sizes typically represent revenue amounts</li>
                <li>🔄 <strong>Animations</strong>: Use play/pause controls for timeline visualizations</li>
                <li>📱 <strong>Mobile Friendly</strong>: All charts work on mobile devices</li>
                <li>💾 <strong>Download</strong>: Hover over charts and click camera icon to save images</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# APPLICATION ENTRY POINT
# ==============================================================================
def main():
    """Main entry point for the application"""
    try:
        app = MovieRevenueTracker()
        app.run()
    except Exception as e:
        st.error(f"❌ Application Error: {str(e)}")
        st.info("💡 Please check if all required files are present and try refreshing the page.")

if __name__ == "__main__":
    main()
