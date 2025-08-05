import pandas as pd
import numpy as np
import streamlit as st
from typing import Optional, Tuple, List
from src.config.settings import FINANCIAL_COLUMNS, NUMERIC_COLUMNS, PERFORMANCE_CATEGORIES

class DataProcessor:
    """Class to handle data loading, cleaning, and processing operations"""
    
    def __init__(self, csv_file_path: str = 'movie_revenue_data.csv'):
        self.csv_file_path = csv_file_path
        self.df = None
    
    @st.cache_data
    def load_data(_self) -> Optional[pd.DataFrame]:
        """
        Load movie revenue data - wrapper for load_and_clean_data
        
        Returns:
            pd.DataFrame: Loaded and cleaned dataset
        """
        return _self.load_and_clean_data()
    
    @st.cache_data
    def load_and_clean_data(_self) -> Optional[pd.DataFrame]:
        """
        Load and clean the movie box office dataset for regional analysis
        
        Returns:
            pd.DataFrame: Cleaned dataset or None if error occurs
        """
        try:
            df = pd.read_csv(_self.csv_file_path)
            
            if df.empty:
                st.error("❌ Dataset is empty!")
                return None
            
            # Clean column names
            df.columns = df.columns.str.strip()
            
            # Convert financial columns to numeric
            for col in FINANCIAL_COLUMNS:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Convert other numeric columns
            for col in NUMERIC_COLUMNS:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Extract rating scores
            if 'Rating' in df.columns:
                df['Rating_Score'] = df['Rating'].str.extract(r'(\d+\.?\d*)').astype(float)
            
            # Clean genres
            if 'Genres' in df.columns:
                df['Primary_Genre'] = df['Genres'].str.split(',').str[0].str.strip()
            
            # Add regional analysis columns
            df = _self._add_calculated_columns(df)
            
            # Remove rows with missing critical data
            df = df.dropna(subset=['$Worldwide', 'Year'])
            
            _self.df = df
            return df
            
        except FileNotFoundError:
            st.error(f"❌ Dataset file '{_self.csv_file_path}' not found!")
            return None
        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")
            return None
    
    def _add_calculated_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add calculated columns for regional analysis
        
        Args:
            df: Original dataframe
            
        Returns:
            pd.DataFrame: Dataframe with additional calculated columns
        """
        # Convert to millions for easier reading
        df['Worldwide_Millions'] = df['$Worldwide'] / 1_000_000
        df['Domestic_Millions'] = df['$Domestic'] / 1_000_000
        df['Foreign_Millions'] = df['$Foreign'] / 1_000_000
        
        # Time-based groupings
        df['Decade'] = (df['Year'] // 10) * 10
        
        # Regional performance indicators
        df['Domestic_Dominance'] = df['Domestic %'] > 50
        df['Foreign_Dominance'] = df['Foreign %'] > 50
        df['Regional_Balance'] = ((df['Domestic %'] - 50).abs() <= 10)
        
        # Performance categories
        df['Performance_Category'] = pd.cut(
            df['Worldwide_Millions'], 
            bins=[0, 100, 500, 1000, float('inf')],
            labels=PERFORMANCE_CATEGORIES
        )
        
        # Regional preference ratio
        df['Domestic_Foreign_Ratio'] = df['$Domestic'] / df['$Foreign'].replace(0, 1)
        
        # Revenue growth indicators
        if len(df) > 1:
            df['Revenue_Rank'] = df['$Worldwide'].rank(ascending=False)
            df['Domestic_Rank'] = df['$Domestic'].rank(ascending=False)
            df['Foreign_Rank'] = df['$Foreign'].rank(ascending=False)
        
        return df
    
    def apply_filters(self, 
                     df: pd.DataFrame,
                     year_range: Tuple[int, int],
                     selected_genre: str = "All",
                     selected_language: str = "All",
                     regional_filter: str = "All",
                     revenue_range: Tuple[float, float] = None) -> pd.DataFrame:
        """
        Apply filters to the dataframe
        
        Args:
            df: Source dataframe
            year_range: Tuple of (min_year, max_year)
            selected_genre: Selected genre filter
            selected_language: Selected language filter
            regional_filter: Regional performance filter
            revenue_range: Revenue range filter
            
        Returns:
            pd.DataFrame: Filtered dataframe
        """
        filtered_df = df.copy()
        
        # Year filter
        filtered_df = filtered_df[
            (filtered_df['Year'] >= year_range[0]) & 
            (filtered_df['Year'] <= year_range[1])
        ]
        
        # Genre filter
        if selected_genre != "All" and 'Primary_Genre' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Primary_Genre'] == selected_genre]
        
        # Language filter
        if selected_language != "All" and 'Original_Language' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Original_Language'] == selected_language]
        
        # Regional performance filter
        if regional_filter == "Domestic Dominance (>50%)":
            filtered_df = filtered_df[filtered_df['Domestic_Dominance'] == True]
        elif regional_filter == "Foreign Dominance (>50%)":
            filtered_df = filtered_df[filtered_df['Foreign_Dominance'] == True]
        elif regional_filter == "Balanced Performance":
            filtered_df = filtered_df[filtered_df['Regional_Balance'] == True]
        
        # Revenue filter
        if revenue_range:
            filtered_df = filtered_df[
                (filtered_df['Worldwide_Millions'] >= revenue_range[0]) &
                (filtered_df['Worldwide_Millions'] <= revenue_range[1])
            ]
        
        return filtered_df
    
    def get_summary_stats(self, df: pd.DataFrame) -> dict:
        """
        Get summary statistics for the dataset
        
        Args:
            df: Source dataframe
            
        Returns:
            dict: Summary statistics
        """
        if df.empty:
            return {}
        
        stats = {
            'total_movies': len(df),
            'total_worldwide_revenue': df['$Worldwide'].sum(),
            'avg_worldwide_revenue': df['$Worldwide'].mean(),
            'avg_domestic_percentage': df['Domestic %'].mean(),
            'avg_foreign_percentage': df['Foreign %'].mean(),
            'top_grossing_movie': df.loc[df['$Worldwide'].idxmax(), 'Release Group'] if not df.empty else "N/A",
            'avg_rating': df['Rating_Score'].mean() if 'Rating_Score' in df.columns and not df['Rating_Score'].isna().all() else 0,
            'year_range': (int(df['Year'].min()), int(df['Year'].max())),
            'unique_genres': df['Primary_Genre'].nunique() if 'Primary_Genre' in df.columns else 0,
            'domestic_dominance_count': len(df[df['Domestic_Dominance'] == True]),
            'foreign_dominance_count': len(df[df['Foreign_Dominance'] == True]),
            'balanced_performance_count': len(df[df['Regional_Balance'] == True])
        }
        
        return stats
    
    def get_top_performers(self, df: pd.DataFrame, n: int = 10, by: str = 'worldwide') -> pd.DataFrame:
        """
        Get top performing movies by specified criteria
        
        Args:
            df: Source dataframe
            n: Number of top movies to return
            by: Criteria for ranking ('worldwide', 'domestic', 'foreign')
            
        Returns:
            pd.DataFrame: Top performing movies
        """
        if df.empty:
            return pd.DataFrame()
        
        sort_column_map = {
            'worldwide': '$Worldwide',
            'domestic': '$Domestic', 
            'foreign': '$Foreign'
        }
        
        sort_column = sort_column_map.get(by, '$Worldwide')
        
        if sort_column not in df.columns:
            return pd.DataFrame()
        
        return df.nlargest(n, sort_column)
    
    def get_genre_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Get genre-wise analysis data
        
        Args:
            df: Source dataframe
            
        Returns:
            pd.DataFrame: Genre analysis summary
        """
        if df.empty or 'Primary_Genre' not in df.columns:
            return pd.DataFrame()
        
        genre_stats = df.groupby('Primary_Genre').agg({
            'Worldwide_Millions': ['count', 'mean', 'sum', 'std'],
            'Domestic %': 'mean',
            'Foreign %': 'mean',
            'Rating_Score': 'mean' if 'Rating_Score' in df.columns else lambda x: 0
        }).round(2)
        
        # Flatten column names
        genre_stats.columns = [
            'Movie_Count', 'Avg_Revenue_M', 'Total_Revenue_M', 'Revenue_Std',
            'Avg_Domestic_Pct', 'Avg_Foreign_Pct', 'Avg_Rating'
        ]
        
        genre_stats = genre_stats.reset_index()
        genre_stats = genre_stats.sort_values('Total_Revenue_M', ascending=False)
        
        return genre_stats
    
    def get_yearly_trends(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Get yearly trend analysis
        
        Args:
            df: Source dataframe
            
        Returns:
            pd.DataFrame: Yearly trends summary
        """
        if df.empty:
            return pd.DataFrame()
        
        yearly_trends = df.groupby('Year').agg({
            'Worldwide_Millions': ['count', 'mean', 'sum'],
            'Domestic %': 'mean',
            'Foreign %': 'mean',
            'Rating_Score': 'mean' if 'Rating_Score' in df.columns else lambda x: 0
        }).round(2)
        
        # Flatten column names
        yearly_trends.columns = [
            'Movie_Count', 'Avg_Revenue_M', 'Total_Revenue_M',
            'Avg_Domestic_Pct', 'Avg_Foreign_Pct', 'Avg_Rating'
        ]
        
        yearly_trends = yearly_trends.reset_index()
        
        return yearly_trends
    
    def filter_data(self, data: pd.DataFrame, selected_movies: List[str], 
                   selected_regions: List[str], revenue_range: Tuple[float, float]) -> pd.DataFrame:
        """
        Filter data based on user selections
        
        Args:
            data: Original dataframe
            selected_movies: List of selected movie titles
            selected_regions: List of selected regions
            revenue_range: Tuple of (min_revenue, max_revenue)
            
        Returns:
            pd.DataFrame: Filtered dataframe
        """
        filtered_data = data.copy()
        
        # Filter by movies
        if 'All Movies' not in selected_movies and selected_movies:
            filtered_data = filtered_data[filtered_data['Movie'].isin(selected_movies)]
        
        # Filter by revenue range
        min_revenue, max_revenue = revenue_range
        filtered_data = filtered_data[
            (filtered_data['Worldwide'] >= min_revenue) & 
            (filtered_data['Worldwide'] <= max_revenue)
        ]
        
        # Note: Region filtering is handled in the visualization layer
        # since it affects which columns to display rather than which rows to show
        
        return filtered_data
