import streamlit as st
import pandas as pd
from typing import List, Tuple, Optional, Dict, Any
from src.config.settings import ALL_OPTION, REGIONAL_FILTERS, ANALYSIS_TYPES

class UIComponents:
    """Class containing reusable UI components"""
    
    @staticmethod
    def create_metric_card(title: str, value: str, icon: str, description: str = "") -> str:
        """
        Create HTML for a metric card
        
        Args:
            title: Card title
            value: Main value to display
            icon: Emoji icon
            description: Optional description
            
        Returns:
            str: HTML string for metric card
        """
        return f"""
        <div class="metric-card animated-element">
            <h3>{icon}</h3>
            <h2>{value}</h2>
            <p>{title}</p>
            {f'<small>{description}</small>' if description else ''}
        </div>
        """
    
    @staticmethod
    def create_header(title: str, subtitle: str = "") -> None:
        """
        Create main header section
        
        Args:
            title: Main title
            subtitle: Optional subtitle
        """
        st.markdown(f"""
        <div class="animated-element">
            <h1 class="main-header">{title}</h1>
            {f'<p class="sub-header">{subtitle}</p>' if subtitle else ''}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_analysis_header(title: str) -> None:
        """
        Create analysis section header
        
        Args:
            title: Analysis section title
        """
        st.markdown(f'<h2 class="analysis-header">{title}</h2>', unsafe_allow_html=True)
    
    @staticmethod
    def create_sidebar_filters(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Create sidebar filter controls
        
        Args:
            df: Source dataframe
            
        Returns:
            dict: Dictionary containing all filter values
        """
        st.sidebar.markdown("### 🌍 Regional Analysis Controls")
        
        # Year range filter
        if 'Year' in df.columns:
            min_year, max_year = int(df['Year'].min()), int(df['Year'].max())
            year_range = st.sidebar.slider(
                "📅 Release Year Range", 
                min_year, max_year, (min_year, max_year)
            )
        else:
            year_range = (2000, 2023)
        
        # Genre filter
        selected_genre = ALL_OPTION
        if 'Primary_Genre' in df.columns:
            genres = [ALL_OPTION] + sorted(df['Primary_Genre'].dropna().unique())
            selected_genre = st.sidebar.selectbox("🎭 Movie Genre", genres)
        
        # Language filter
        selected_language = ALL_OPTION
        if 'Original_Language' in df.columns:
            languages = [ALL_OPTION] + sorted(df['Original_Language'].dropna().unique())
            selected_language = st.sidebar.selectbox("🗣️ Original Language", languages)
        
        # Regional performance filter
        regional_filter = st.sidebar.selectbox(
            "🌍 Regional Performance Focus",
            REGIONAL_FILTERS
        )
        
        # Revenue range filter
        if 'Worldwide_Millions' in df.columns:
            min_revenue = float(df['Worldwide_Millions'].min())
            max_revenue = float(df['Worldwide_Millions'].max())
            revenue_range = st.sidebar.slider(
                "💰 Worldwide Revenue Range (M USD)",
                min_revenue, max_revenue, (min_revenue, max_revenue)
            )
        else:
            revenue_range = (0.0, 1000.0)
        
        # Display options
        st.sidebar.markdown("### 📊 Display Options")
        show_top_n = st.sidebar.number_input("🔢 Show Top N Movies", 5, 50, 15)
        analysis_type = st.sidebar.radio("🔍 Analysis Focus", ANALYSIS_TYPES)
        
        return {
            'year_range': year_range,
            'selected_genre': selected_genre,
            'selected_language': selected_language,
            'regional_filter': regional_filter,
            'revenue_range': revenue_range,
            'show_top_n': show_top_n,
            'analysis_type': analysis_type
        }
    
    @staticmethod
    def create_metrics_row(stats: Dict[str, Any]) -> None:
        """
        Create metrics row with key statistics
        
        Args:
            stats: Dictionary containing statistics
        """
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            value = f"{stats.get('total_movies', 0):,}"
            st.markdown(UIComponents.create_metric_card(
                "Total Movies", value, "🎬"
            ), unsafe_allow_html=True)
        
        with col2:
            avg_revenue = stats.get('avg_worldwide_revenue', 0) / 1_000_000
            value = f"${avg_revenue:.1f}M"
            st.markdown(UIComponents.create_metric_card(
                "Avg Worldwide", value, "💰"
            ), unsafe_allow_html=True)
        
        with col3:
            avg_domestic = stats.get('avg_domestic_percentage', 0)
            value = f"{avg_domestic:.1f}%"
            st.markdown(UIComponents.create_metric_card(
                "Avg Domestic", value, "🇺🇸"
            ), unsafe_allow_html=True)
        
        with col4:
            avg_foreign = stats.get('avg_foreign_percentage', 0)
            value = f"{avg_foreign:.1f}%"
            st.markdown(UIComponents.create_metric_card(
                "Avg Foreign", value, "🌍"
            ), unsafe_allow_html=True)
    
    @staticmethod
    def create_extended_metrics_row(stats: Dict[str, Any]) -> None:
        """
        Create extended metrics row with additional statistics
        
        Args:
            stats: Dictionary containing statistics
        """
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            value = f"{stats.get('total_movies', 0):,}"
            st.markdown(UIComponents.create_metric_card(
                "Total Movies", value, "🎭"
            ), unsafe_allow_html=True)
        
        with col2:
            total_revenue = stats.get('total_worldwide_revenue', 0) / 1_000_000_000
            value = f"${total_revenue:.1f}B"
            st.markdown(UIComponents.create_metric_card(
                "Total Box Office", value, "💰"
            ), unsafe_allow_html=True)
        
        with col3:
            avg_revenue = stats.get('avg_worldwide_revenue', 0) / 1_000_000
            value = f"${avg_revenue:.0f}M"
            st.markdown(UIComponents.create_metric_card(
                "Avg Revenue", value, "📊"
            ), unsafe_allow_html=True)
        
        with col4:
            avg_rating = stats.get('avg_rating', 0)
            value = f"{avg_rating:.1f}"
            st.markdown(UIComponents.create_metric_card(
                "Avg Rating", value, "⭐"
            ), unsafe_allow_html=True)
        
        with col5:
            top_movie = stats.get('top_grossing_movie', 'N/A')
            display_title = top_movie[:15] + '...' if len(top_movie) > 15 else top_movie
            st.markdown(UIComponents.create_metric_card(
                "Top Movie", display_title, "🏆"
            ), unsafe_allow_html=True)
    
    @staticmethod
    def create_info_box(title: str, content: str, box_type: str = "info") -> None:
        """
        Create an information box
        
        Args:
            title: Box title
            content: Box content
            box_type: Type of box ('info', 'success', 'warning', 'danger')
        """
        icon_map = {
            'info': '💡',
            'success': '✅', 
            'warning': '⚠️',
            'danger': '❌'
        }
        
        icon = icon_map.get(box_type, '💡')
        
        st.markdown(f"""
        <div class="content-card">
            <h4>{icon} {title}</h4>
            <p>{content}</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_data_table(df: pd.DataFrame, title: str = "", max_rows: int = 10) -> None:
        """
        Create a styled data table
        
        Args:
            df: Dataframe to display
            title: Optional table title
            max_rows: Maximum rows to display
        """
        if title:
            st.subheader(title)
        
        if df.empty:
            st.warning("No data available to display")
            return
        
        # Limit rows if needed
        display_df = df.head(max_rows) if len(df) > max_rows else df
        
        st.dataframe(display_df, use_container_width=True)
        
        if len(df) > max_rows:
            st.caption(f"Showing {max_rows} of {len(df)} rows")
    
    @staticmethod
    def create_movie_selector(df: pd.DataFrame, top_n: int = 15) -> List[str]:
        """
        Create movie selector widget
        
        Args:
            df: Source dataframe
            top_n: Number of top movies to show as options
            
        Returns:
            List[str]: Selected movie names
        """
        if df.empty or 'Release Group' not in df.columns:
            st.warning("No movies available for selection")
            return []
        
        top_movies = df.nlargest(top_n, 'Worldwide_Millions')['Release Group'].tolist()
        
        selected_movies = st.multiselect(
            "📽️ Select Movies for Comparison",
            options=top_movies,
            default=top_movies[:5],
            help="Choose movies to compare their regional performance"
        )
        
        return selected_movies
    
    @staticmethod
    def create_download_button(df: pd.DataFrame, filename: str = "movie_data.csv") -> None:
        """
        Create download button for data
        
        Args:
            df: Dataframe to download
            filename: Download filename
        """
        if df.empty:
            return
        
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name=filename,
            mime="text/csv",
            help="Download the current filtered data"
        )
    
    @staticmethod
    def create_filter_summary(filters: Dict[str, Any]) -> None:
        """
        Create a summary of applied filters
        
        Args:
            filters: Dictionary of filter values
        """
        active_filters = []
        
        # Check year range
        year_range = filters.get('year_range', (2000, 2023))
        if year_range != (2000, 2023):
            active_filters.append(f"Year: {year_range[0]}-{year_range[1]}")
        
        # Check genre
        if filters.get('selected_genre', ALL_OPTION) != ALL_OPTION:
            active_filters.append(f"Genre: {filters['selected_genre']}")
        
        # Check language
        if filters.get('selected_language', ALL_OPTION) != ALL_OPTION:
            active_filters.append(f"Language: {filters['selected_language']}")
        
        # Check regional filter
        if filters.get('regional_filter', ALL_OPTION) != ALL_OPTION:
            active_filters.append(f"Region: {filters['regional_filter']}")
        
        if active_filters:
            filter_text = " | ".join(active_filters)
            st.caption(f"🔍 Active Filters: {filter_text}")
        else:
            st.caption("🔍 No filters applied - showing all data")
    
    @staticmethod
    def create_loading_placeholder() -> None:
        """Create loading placeholder"""
        st.markdown("""
        <div class="loading">
            <h3>🔄 Loading data...</h3>
            <p>Please wait while we process your request.</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_error_message(message: str) -> None:
        """
        Create error message display
        
        Args:
            message: Error message to display
        """
        st.error(f"❌ {message}")
    
    @staticmethod
    def create_success_message(message: str) -> None:
        """
        Create success message display
        
        Args:
            message: Success message to display
        """
        st.success(f"✅ {message}")
    
    @staticmethod
    def create_warning_message(message: str) -> None:
        """
        Create warning message display
        
        Args:
            message: Warning message to display
        """
        st.warning(f"⚠️ {message}")
    
    @staticmethod
    def create_footer() -> None:
        """Create application footer"""
        st.markdown("""
        <div class="footer">
            <p>🎬 Movie Revenue Tracker - Regional Analysis Platform</p>
            <p>Powered by Streamlit & Plotly | Data-driven Box Office Insights</p>
        </div>
        """, unsafe_allow_html=True)
