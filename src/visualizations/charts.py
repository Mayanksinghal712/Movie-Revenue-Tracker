import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import List, Optional
import plotly.figure_factory as ff
from src.config.settings import CHART_CONFIG, COLORS

class ChartCreator:
    """Class to create various charts and visualizations"""
    
    def __init__(self):
        self.chart_config = CHART_CONFIG
        self.colors = COLORS
    
    def create_regional_comparison_chart(self, df: pd.DataFrame, selected_movies: List[str]) -> go.Figure:
        """
        Create regional comparison chart for selected movies
        
        Args:
            df: Source dataframe
            selected_movies: List of movie names to compare
            
        Returns:
            go.Figure: Regional comparison chart
        """
        if df.empty or not selected_movies:
            return self._create_empty_chart("No data available for comparison")
        
        movie_data = df[df['Release Group'].isin(selected_movies)].head(10)
        
        if movie_data.empty:
            return self._create_empty_chart("Selected movies not found in data")
        
        fig = go.Figure()
        
        # Domestic Revenue
        fig.add_trace(go.Bar(
            name='Domestic Revenue',
            x=movie_data['Release Group'],
            y=movie_data['Domestic_Millions'],
            marker_color=self.colors['primary'],
            text=movie_data['Domestic_Millions'].round(1),
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Domestic: $%{y:.1f}M<extra></extra>'
        ))
        
        # Foreign Revenue
        fig.add_trace(go.Bar(
            name='Foreign Revenue',
            x=movie_data['Release Group'],
            y=movie_data['Foreign_Millions'],
            marker_color=self.colors['success'],
            text=movie_data['Foreign_Millions'].round(1),
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Foreign: $%{y:.1f}M<extra></extra>'
        ))
        
        fig.update_layout(
            title="Regional Box Office Comparison",
            xaxis_title="Movies",
            yaxis_title="Revenue (Millions USD)",
            barmode='group',
            template=self.chart_config['template'],
            font_family=self.chart_config['font_family'],
            font_size=self.chart_config['font_size'],
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=self.chart_config['height'],
            xaxis_tickangle=-45
        )
        
        return fig
    
    def create_performance_scatter(self, df: pd.DataFrame, size_limit: int = 100) -> go.Figure:
        """
        Create performance scatter plot
        
        Args:
            df: Source dataframe
            size_limit: Maximum number of points to display
            
        Returns:
            go.Figure: Performance scatter plot
        """
        if df.empty:
            return self._create_empty_chart("No data available for scatter plot")
        
        plot_data = df.head(size_limit)
        
        fig = px.scatter(
            plot_data,
            x='Domestic_Millions',
            y='Foreign_Millions',
            size='Worldwide_Millions',
            color='Primary_Genre' if 'Primary_Genre' in plot_data.columns else None,
            hover_data=['Release Group', 'Year'],
            title="Domestic vs Foreign Performance",
            template=self.chart_config['template'],
            color_discrete_sequence=self.chart_config['color_sequence']
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family=self.chart_config['font_family'],
            font_size=self.chart_config['font_size'],
            height=self.chart_config['height']
        )
        
        return fig
    
    def create_genre_regional_analysis(self, df: pd.DataFrame) -> go.Figure:
        """
        Create genre-wise regional analysis chart
        
        Args:
            df: Source dataframe
            
        Returns:
            go.Figure: Genre regional analysis chart
        """
        if df.empty or 'Primary_Genre' not in df.columns:
            return self._create_empty_chart("No genre data available")
        
        genre_stats = df.groupby('Primary_Genre').agg({
            'Domestic %': 'mean',
            'Foreign %': 'mean',
            'Worldwide_Millions': 'mean'
        }).round(2).reset_index()
        
        if genre_stats.empty:
            return self._create_empty_chart("No genre statistics available")
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Avg Domestic %',
            x=genre_stats['Primary_Genre'],
            y=genre_stats['Domestic %'],
            marker_color=self.colors['primary'],
            hovertemplate='<b>%{x}</b><br>Domestic: %{y:.1f}%<extra></extra>'
        ))
        
        fig.add_trace(go.Bar(
            name='Avg Foreign %',
            x=genre_stats['Primary_Genre'],
            y=genre_stats['Foreign %'],
            marker_color=self.colors['success'],
            hovertemplate='<b>%{x}</b><br>Foreign: %{y:.1f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title="Genre-wise Regional Performance",
            xaxis_title="Genre",
            yaxis_title="Average Percentage",
            template=self.chart_config['template'],
            font_family=self.chart_config['font_family'],
            font_size=self.chart_config['font_size'],
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=self.chart_config['height'],
            xaxis_tickangle=-45
        )
        
        return fig
    
    def create_revenue_trends_chart(self, df: pd.DataFrame) -> go.Figure:
        """
        Create revenue trends over time chart
        
        Args:
            df: Source dataframe
            
        Returns:
            go.Figure: Revenue trends chart
        """
        if df.empty:
            return self._create_empty_chart("No data available for trends")
        
        yearly_trends = df.groupby('Year').agg({
            'Domestic %': 'mean',
            'Foreign %': 'mean',
            'Worldwide_Millions': 'mean',
            'Release Group': 'count'
        }).reset_index()
        
        if yearly_trends.empty:
            return self._create_empty_chart("No yearly trends data available")
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add domestic percentage trend
        fig.add_trace(
            go.Scatter(
                x=yearly_trends['Year'],
                y=yearly_trends['Domestic %'],
                mode='lines+markers',
                name='Domestic %',
                line=dict(color=self.colors['primary'], width=3),
                hovertemplate='<b>Year: %{x}</b><br>Domestic: %{y:.1f}%<extra></extra>'
            ),
            secondary_y=False,
        )
        
        # Add foreign percentage trend
        fig.add_trace(
            go.Scatter(
                x=yearly_trends['Year'],
                y=yearly_trends['Foreign %'],
                mode='lines+markers',
                name='Foreign %',
                line=dict(color=self.colors['success'], width=3),
                hovertemplate='<b>Year: %{x}</b><br>Foreign: %{y:.1f}%<extra></extra>'
            ),
            secondary_y=False,
        )
        
        # Add movie count as bars on secondary y-axis
        fig.add_trace(
            go.Bar(
                x=yearly_trends['Year'],
                y=yearly_trends['Release Group'],
                name='Number of Movies',
                opacity=0.6,
                marker_color=self.colors['warning'],
                hovertemplate='<b>Year: %{x}</b><br>Movies: %{y}<extra></extra>'
            ),
            secondary_y=True,
        )
        
        fig.update_layout(
            title="Regional Market Share Trends Over Time",
            template=self.chart_config['template'],
            height=self.chart_config['height'],
            font_family=self.chart_config['font_family'],
            font_size=self.chart_config['font_size'],
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        fig.update_xaxes(title_text="Year")
        fig.update_yaxes(title_text="Average Percentage", secondary_y=False)
        fig.update_yaxes(title_text="Number of Movies", secondary_y=True)
        
        return fig
    
    def create_top_performers_chart(self, df: pd.DataFrame, n: int = 10, orientation: str = 'h') -> go.Figure:
        """
        Create top performers chart
        
        Args:
            df: Source dataframe
            n: Number of top performers to show
            orientation: Chart orientation ('h' for horizontal, 'v' for vertical)
            
        Returns:
            go.Figure: Top performers chart
        """
        if df.empty:
            return self._create_empty_chart("No data available for top performers")
        
        top_movies = df.nlargest(n, 'Worldwide_Millions')
        
        if orientation == 'h':
            fig = px.bar(
                top_movies,
                x='Worldwide_Millions',
                y='Release Group',
                orientation='h',
                title=f"Top {n} Movies by Worldwide Revenue",
                labels={'Worldwide_Millions': 'Revenue (Million USD)', 'Release Group': 'Movie'},
                color='Worldwide_Millions',
                color_continuous_scale='viridis',
                template=self.chart_config['template']
            )
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        else:
            fig = px.bar(
                top_movies,
                x='Release Group',
                y='Worldwide_Millions',
                title=f"Top {n} Movies by Worldwide Revenue",
                labels={'Worldwide_Millions': 'Revenue (Million USD)', 'Release Group': 'Movie'},
                color='Worldwide_Millions',
                color_continuous_scale='viridis',
                template=self.chart_config['template']
            )
            fig.update_layout(xaxis_tickangle=-45)
        
        fig.update_layout(
            height=self.chart_config['height'],
            font_family=self.chart_config['font_family'],
            font_size=self.chart_config['font_size'],
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_pie_chart(self, data: dict, title: str) -> go.Figure:
        """
        Create a pie chart
        
        Args:
            data: Dictionary with labels as keys and values as values
            title: Chart title
            
        Returns:
            go.Figure: Pie chart
        """
        if not data:
            return self._create_empty_chart("No data available for pie chart")
        
        fig = px.pie(
            values=list(data.values()),
            names=list(data.keys()),
            title=title,
            color_discrete_sequence=self.chart_config['color_sequence'],
            template=self.chart_config['template']
        )
        
        fig.update_layout(
            font_family=self.chart_config['font_family'],
            font_size=self.chart_config['font_size'],
            height=self.chart_config['height']
        )
        
        return fig
    
    def create_stacked_bar_chart(self, df: pd.DataFrame, x_col: str, y_cols: List[str], title: str) -> go.Figure:
        """
        Create a stacked bar chart
        
        Args:
            df: Source dataframe
            x_col: Column for x-axis
            y_cols: Columns for y-axis (stacked)
            title: Chart title
            
        Returns:
            go.Figure: Stacked bar chart
        """
        if df.empty:
            return self._create_empty_chart("No data available for stacked bar chart")
        
        fig = go.Figure()
        
        colors = [self.colors['primary'], self.colors['secondary'], self.colors['success'], 
                 self.colors['warning'], self.colors['danger'], self.colors['info']]
        
        for i, col in enumerate(y_cols):
            if col in df.columns:
                fig.add_trace(go.Bar(
                    name=col,
                    x=df[x_col],
                    y=df[col],
                    marker_color=colors[i % len(colors)],
                    hovertemplate=f'<b>%{{x}}</b><br>{col}: %{{y}}<extra></extra>'
                ))
        
        fig.update_layout(
            title=title,
            barmode='stack',
            template=self.chart_config['template'],
            font_family=self.chart_config['font_family'],
            font_size=self.chart_config['font_size'],
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=self.chart_config['height'],
            xaxis_tickangle=-45
        )
        
        return fig
    
    def _create_empty_chart(self, message: str) -> go.Figure:
        """
        Create an empty chart with a message
        
        Args:
            message: Message to display
            
        Returns:
            go.Figure: Empty chart with message
        """
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            xanchor='center', yanchor='middle',
            showarrow=False,
            font_size=16,
            font_color=self.colors['text_muted']
        )
        fig.update_layout(
            template=self.chart_config['template'],
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis={'visible': False},
            yaxis={'visible': False}
        )
        return fig
    
    def create_advanced_3d_scatter(self, df: pd.DataFrame) -> go.Figure:
        """
        Create stunning 3D scatter plot with animated bubbles
        
        Args:
            df: Source dataframe
            
        Returns:
            go.Figure: Advanced 3D scatter plot
        """
        if df.empty:
            return self._create_empty_chart("No data available for 3D visualization")
        
        plot_data = df.head(50)  # Limit for performance
        
        # Create color mapping for genres
        unique_genres = plot_data['Primary_Genre'].unique() if 'Primary_Genre' in plot_data.columns else ['Unknown']
        color_scale = px.colors.qualitative.Set3
        
        fig = go.Figure()
        
        for i, genre in enumerate(unique_genres):
            genre_data = plot_data[plot_data['Primary_Genre'] == genre] if 'Primary_Genre' in plot_data.columns else plot_data
            
            fig.add_trace(go.Scatter3d(
                x=genre_data['Domestic_Millions'],
                y=genre_data['Foreign_Millions'],
                z=genre_data['Year'],
                mode='markers',
                marker=dict(
                    size=genre_data['Worldwide_Millions'] / 50,
                    color=color_scale[i % len(color_scale)],
                    opacity=0.8,
                    line=dict(color='white', width=2),
                    sizemode='diameter'
                ),
                text=genre_data['Release Group'],
                hovertemplate='<b>%{text}</b><br>' +
                             'Domestic: $%{x:.1f}M<br>' +
                             'Foreign: $%{y:.1f}M<br>' +
                             'Year: %{z}<br>' +
                             '<extra></extra>',
                name=genre
            ))
        
        fig.update_layout(
            title={
                'text': "🎬 3D Movie Performance Universe",
                'x': 0.5,
                'font': {'size': 20, 'color': '#00D4FF'}
            },
            scene=dict(
                xaxis_title="Domestic Revenue (M$)",
                yaxis_title="Foreign Revenue (M$)",
                zaxis_title="Release Year",
                bgcolor='rgba(0,0,0,0)',
                xaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(255,255,255,0.2)'),
                yaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(255,255,255,0.2)'),
                zaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(255,255,255,0.2)')
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=600,
            showlegend=True
        )
        
        return fig
    
    def create_animated_timeline_chart(self, df: pd.DataFrame) -> go.Figure:
        """
        Create animated timeline chart showing movie trends over years
        
        Args:
            df: Source dataframe
            
        Returns:
            go.Figure: Animated timeline chart
        """
        if df.empty:
            return self._create_empty_chart("No data available for timeline")
        
        # Prepare data for animation
        yearly_data = df.groupby(['Year', 'Primary_Genre']).agg({
            'Worldwide_Millions': ['sum', 'count'],
            'Domestic_Millions': 'sum',
            'Foreign_Millions': 'sum'
        }).round(2)
        
        yearly_data.columns = ['Total_Revenue', 'Movie_Count', 'Domestic_Total', 'Foreign_Total']
        yearly_data = yearly_data.reset_index()
        
        fig = px.scatter(
            yearly_data,
            x='Domestic_Total',
            y='Foreign_Total',
            size='Total_Revenue',
            color='Primary_Genre',
            animation_frame='Year',
            hover_name='Primary_Genre',
            size_max=60,
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
        
        fig.update_traces(
            marker=dict(
                line=dict(width=2, color='white'),
                opacity=0.8
            )
        )
        
        fig.update_layout(
            title={
                'text': "🎭 Animated Genre Evolution Timeline",
                'x': 0.5,
                'font': {'size': 20, 'color': '#FF6B6B'}
            },
            xaxis_title="Domestic Revenue (M$)",
            yaxis_title="Foreign Revenue (M$)",
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=600,
            showlegend=True
        )
        
        return fig
    
    def create_radial_chart(self, df: pd.DataFrame) -> go.Figure:
        """
        Create beautiful radial/polar chart for genre performance
        
        Args:
            df: Source dataframe
            
        Returns:
            go.Figure: Radial chart
        """
        if df.empty or 'Primary_Genre' not in df.columns:
            return self._create_empty_chart("No genre data available for radial chart")
        
        genre_stats = df.groupby('Primary_Genre').agg({
            'Worldwide_Millions': 'mean',
            'Domestic %': 'mean',
            'Foreign %': 'mean'
        }).round(2).reset_index()
        
        fig = go.Figure()
        
        # Add radial bar chart
        fig.add_trace(go.Barpolar(
            r=genre_stats['Worldwide_Millions'],
            theta=genre_stats['Primary_Genre'],
            name='Avg Revenue',
            marker_color=px.colors.sequential.Plasma,
            marker_line_color="white",
            marker_line_width=2,
            opacity=0.8
        ))
        
        fig.update_layout(
            title={
                'text': "🌟 Genre Performance Radar",
                'x': 0.5,
                'font': {'size': 20, 'color': '#FFD700'}
            },
            template='plotly_dark',
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, genre_stats['Worldwide_Millions'].max() * 1.1],
                    gridcolor='rgba(255,255,255,0.3)'
                ),
                angularaxis=dict(
                    gridcolor='rgba(255,255,255,0.3)',
                    tickfont=dict(color='white')
                ),
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=600
        )
        
        return fig
    
    def create_waterfall_chart(self, df: pd.DataFrame, selected_movie: str) -> go.Figure:
        """
        Create waterfall chart showing revenue breakdown
        
        Args:
            df: Source dataframe
            selected_movie: Movie to analyze
            
        Returns:
            go.Figure: Waterfall chart
        """
        if df.empty or not selected_movie:
            return self._create_empty_chart("No movie selected for waterfall analysis")
        
        movie_data = df[df['Release Group'] == selected_movie]
        if movie_data.empty:
            return self._create_empty_chart(f"Movie '{selected_movie}' not found")
        
        movie = movie_data.iloc[0]
        
        fig = go.Figure(go.Waterfall(
            name="Revenue Breakdown",
            orientation="v",
            measure=["relative", "relative", "total"],
            x=["Domestic Revenue", "Foreign Revenue", "Total Worldwide"],
            textposition="outside",
            text=[f"${movie['Domestic_Millions']:.1f}M", 
                  f"${movie['Foreign_Millions']:.1f}M", 
                  f"${movie['Worldwide_Millions']:.1f}M"],
            y=[movie['Domestic_Millions'], movie['Foreign_Millions'], movie['Worldwide_Millions']],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            decreasing={"marker": {"color": "#FF6B6B"}},
            increasing={"marker": {"color": "#4ECDC4"}},
            totals={"marker": {"color": "#45B7D1"}}
        ))
        
        fig.update_layout(
            title={
                'text': f"💰 Revenue Waterfall: {selected_movie}",
                'x': 0.5,
                'font': {'size': 18, 'color': '#4ECDC4'}
            },
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=500,
            yaxis_title="Revenue (Millions USD)"
        )
        
        return fig
    
    def create_heatmap_correlation(self, df: pd.DataFrame) -> go.Figure:
        """
        Create correlation heatmap with beautiful gradients
        
        Args:
            df: Source dataframe
            
        Returns:
            go.Figure: Correlation heatmap
        """
        if df.empty:
            return self._create_empty_chart("No data available for correlation analysis")
        
        # Select numeric columns for correlation
        numeric_cols = ['Worldwide_Millions', 'Domestic_Millions', 'Foreign_Millions', 
                       'Domestic %', 'Foreign %', 'Year']
        numeric_cols = [col for col in numeric_cols if col in df.columns]
        
        if len(numeric_cols) < 2:
            return self._create_empty_chart("Insufficient numeric data for correlation")
        
        corr_matrix = df[numeric_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdYlBu_r',
            zmid=0,
            text=np.round(corr_matrix.values, 2),
            texttemplate="%{text}",
            textfont={"size": 12, "color": "white"},
            hoverongaps=False,
            hovertemplate='<b>%{x} vs %{y}</b><br>Correlation: %{z:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title={
                'text': "🔥 Revenue Metrics Correlation Heatmap",
                'x': 0.5,
                'font': {'size': 18, 'color': '#FF6B6B'}
            },
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=500,
            xaxis=dict(side='bottom')
        )
        
        return fig
    
    def create_sunburst_chart(self, df: pd.DataFrame) -> go.Figure:
        """
        Create stunning sunburst chart for hierarchical data
        
        Args:
            df: Source dataframe
            
        Returns:
            go.Figure: Sunburst chart
        """
        if df.empty:
            return self._create_empty_chart("No data available for sunburst chart")
        
        # Create hierarchical data (Genre -> Rating -> Movies)
        sunburst_data = []
        
        for genre in df['Primary_Genre'].unique() if 'Primary_Genre' in df.columns else ['Unknown']:
            genre_df = df[df['Primary_Genre'] == genre] if 'Primary_Genre' in df.columns else df
            genre_revenue = genre_df['Worldwide_Millions'].sum()
            
            sunburst_data.append({
                'ids': genre,
                'labels': genre,
                'parents': '',
                'values': genre_revenue
            })
            
            for rating in genre_df['Rating'].unique() if 'Rating' in genre_df.columns else ['Unknown']:
                rating_df = genre_df[genre_df['Rating'] == rating] if 'Rating' in genre_df.columns else genre_df
                rating_revenue = rating_df['Worldwide_Millions'].sum()
                
                sunburst_data.append({
                    'ids': f"{genre} - {rating}",
                    'labels': rating,
                    'parents': genre,
                    'values': rating_revenue
                })
        
        sunburst_df = pd.DataFrame(sunburst_data)
        
        fig = go.Figure(go.Sunburst(
            ids=sunburst_df['ids'],
            labels=sunburst_df['labels'],
            parents=sunburst_df['parents'],
            values=sunburst_df['values'],
            branchvalues="total",
            hovertemplate='<b>%{label}</b><br>Revenue: $%{value:.1f}M<extra></extra>',
            maxdepth=3,
            insidetextorientation='radial'
        ))
        
        fig.update_layout(
            title={
                'text': "☀️ Genre & Rating Revenue Sunburst",
                'x': 0.5,
                'font': {'size': 18, 'color': '#FFD700'}
            },
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            height=600
        )
        
        return fig
    
    def create_violin_plot(self, df: pd.DataFrame) -> go.Figure:
        """
        Create violin plot for revenue distribution by genre
        
        Args:
            df: Source dataframe
            
        Returns:
            go.Figure: Violin plot
        """
        if df.empty or 'Primary_Genre' not in df.columns:
            return self._create_empty_chart("No genre data available for violin plot")
        
        fig = go.Figure()
        
        colors = px.colors.qualitative.Set2
        
        for i, genre in enumerate(df['Primary_Genre'].unique()):
            genre_data = df[df['Primary_Genre'] == genre]['Worldwide_Millions']
            
            fig.add_trace(go.Violin(
                y=genre_data,
                name=genre,
                box_visible=True,
                meanline_visible=True,
                fillcolor=colors[i % len(colors)],
                opacity=0.7,
                line_color='white'
            ))
        
        fig.update_layout(
            title={
                'text': "🎻 Revenue Distribution Violin Plot",
                'x': 0.5,
                'font': {'size': 18, 'color': '#9B59B6'}
            },
            yaxis_title="Revenue (Millions USD)",
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=500,
            showlegend=False
        )
        
        return fig
