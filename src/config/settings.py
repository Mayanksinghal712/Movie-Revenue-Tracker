import streamlit as st

# ==============================================================================
# PAGE CONFIGURATION
# ==============================================================================
def configure_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="Movie Revenue Tracker - Regional Analysis",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# ==============================================================================
# DATA CONSTANTS
# ==============================================================================
FINANCIAL_COLUMNS = ['$Worldwide', '$Domestic', '$Foreign', 'Domestic %', 'Foreign %']
NUMERIC_COLUMNS = ['Year', 'Vote_Count']
ANALYSIS_TYPES = [
    "Regional Comparison", 
    "Revenue Performance", 
    "Genre Analysis", 
    "Market Trends",
    "🎨 Advanced Visualizations"
]

# ==============================================================================
# UI CONSTANTS
# ==============================================================================
ALL_OPTION = "All"
DEFAULT_TOP_N = 15
MIN_TOP_N = 5
MAX_TOP_N = 50

# ==============================================================================
# COLOR SCHEME (Dark Mode)
# ==============================================================================
class ColorScheme:
    """Ultra-modern color scheme for cinematic interface"""
    
    # Neon Accent Colors
    NEON_CYAN = '#00d4ff'
    NEON_PURPLE = '#b24cf3'
    NEON_PINK = '#ff006e'
    NEON_GREEN = '#39ff14'
    NEON_ORANGE = '#ff8c00'
    NEON_BLUE = '#1e90ff'
    
    # Traditional Colors
    PRIMARY = '#4facfe'
    SECONDARY = '#00f2fe'
    SUCCESS = '#43e97b'
    WARNING = '#f093fb'
    DANGER = '#ff6b6b'
    INFO = '#4ecdc4'
    
    # Background Colors
    BACKGROUND_DARK = '#1a1a1a'
    BACKGROUND_MEDIUM = '#2d2d2d'
    
    # Text Colors
    TEXT_PRIMARY = '#ffffff'
    TEXT_SECONDARY = '#b0b0b0'
    
    # Color Sequences
    NEON_SEQUENCE = [NEON_CYAN, NEON_PURPLE, NEON_PINK, NEON_GREEN, NEON_ORANGE, NEON_BLUE]
    CHART_SEQUENCE = [PRIMARY, SECONDARY, SUCCESS, WARNING, DANGER, INFO]
    
    @classmethod
    def get_color_by_index(cls, index: int) -> str:
        """Get color by index from neon sequence"""
        return cls.NEON_SEQUENCE[index % len(cls.NEON_SEQUENCE)]

COLORS = {
    'primary': '#4facfe',
    'secondary': '#00f2fe', 
    'success': '#43e97b',
    'warning': '#f093fb',
    'danger': '#ff6b6b',
    'info': '#4ecdc4',
    'dark': '#2c3e50',
    'light': '#ecf0f1',
    'background_dark': '#1a1a1a',
    'background_medium': '#2d2d2d',
    'text_primary': '#ffffff',
    'text_secondary': '#b0b0b0',
    'text_muted': '#666666'
}

# ==============================================================================
# CHART CONFIGURATION
# ==============================================================================
CHART_CONFIG = {
    'template': 'plotly_dark',
    'font_family': 'Poppins',
    'font_size': 12,
    'height': 500,
    'color_sequence': ['#4facfe', '#00f2fe', '#43e97b', '#f093fb', '#ff6b6b', '#4ecdc4']
}

# ==============================================================================
# FILTERS CONFIGURATION
# ==============================================================================
REGIONAL_FILTERS = [
    ALL_OPTION,
    "Domestic Dominance (>50%)", 
    "Foreign Dominance (>50%)", 
    "Balanced Performance"
]

PERFORMANCE_CATEGORIES = [
    'Low (<$100M)', 
    'Medium ($100M-$500M)', 
    'High ($500M-$1B)', 
    'Blockbuster (>$1B)'
]

# ==============================================================================
# CONFIGURATION CLASSES
# ==============================================================================
class AppConfig:
    """Main application configuration"""
    
    # Application Settings
    APP_TITLE = "🎬 Movie Revenue Tracker - Ultra Modern"
    APP_ICON = "🎬"
    PAGE_LAYOUT = "wide"
    SIDEBAR_STATE = "expanded"
    
    # Cache Settings
    CACHE_TTL = 3600  # 1 hour
    MAX_UPLOAD_SIZE = 200  # MB
    
    # Animation Settings
    CHART_ANIMATION_DURATION = 800  # ms
    HOVER_ANIMATION_DURATION = 200  # ms
    
    # Data Settings
    DEFAULT_FILTERS = ["All Movies", "All Regions"]
    SUPPORTED_FORMATS = [".csv", ".xlsx", ".json"]
    
    # Performance Settings
    LAZY_LOADING = True
    OPTIMIZE_CHARTS = True
    CACHE_DATA = True

class ChartConfig:
    """Chart configuration settings"""
    
    # Chart Templates
    TEMPLATE = 'plotly_dark'
    TEMPLATE_ULTRA = 'plotly_dark'
    
    # Typography
    FONT_FAMILY = 'Inter'
    FONT_FAMILY_MONO = 'JetBrains Mono'
    FONT_FAMILY_TITLE = 'Orbitron'
    FONT_SIZE_BASE = 12
    FONT_SIZE_TITLE = 16
    FONT_SIZE_AXIS = 10
    
    # Chart Dimensions
    DEFAULT_HEIGHT = 500
    SMALL_HEIGHT = 300
    LARGE_HEIGHT = 700
    DEFAULT_WIDTH = None  # Auto
    
    # Margins
    MARGIN_TOP = 60
    MARGIN_BOTTOM = 60
    MARGIN_LEFT = 80
    MARGIN_RIGHT = 80
    
    # Colors
    BACKGROUND_COLOR = 'rgba(0,0,0,0)'
    PLOT_BACKGROUND = 'rgba(0,0,0,0)'
    GRID_COLOR = 'rgba(255,255,255,0.1)'
    AXIS_COLOR = 'rgba(255,255,255,0.3)'
    
    # Animation
    ANIMATION_DURATION = 800
    TRANSITION_DURATION = 300
    
    # Interactivity
    HOVER_MODE = 'closest'
    CLICK_MODE = 'event+select'
    DRAG_MODE = 'pan'
    
    # Color Sequences
    NEON_COLORS = ['#00d4ff', '#b24cf3', '#ff006e', '#39ff14', '#ff8c00', '#1e90ff']
    GRADIENT_COLORS = ['#4facfe', '#00f2fe', '#43e97b', '#f093fb', '#ff6b6b', '#4ecdc4']
    
    @classmethod
    def get_base_layout(cls):
        """Get base plotly layout configuration"""
        return {
            'template': cls.TEMPLATE,
            'font': {'family': cls.FONT_FAMILY, 'size': cls.FONT_SIZE_BASE, 'color': 'white'},
            'plot_bgcolor': cls.PLOT_BACKGROUND,
            'paper_bgcolor': cls.BACKGROUND_COLOR,
            'margin': {
                't': cls.MARGIN_TOP,
                'b': cls.MARGIN_BOTTOM,
                'l': cls.MARGIN_LEFT,
                'r': cls.MARGIN_RIGHT
            },
            'height': cls.DEFAULT_HEIGHT,
            'showlegend': True,
            'legend': {
                'orientation': 'h',
                'yanchor': 'bottom',
                'y': 1.02,
                'xanchor': 'right',
                'x': 1
            },
            'xaxis': {
                'gridcolor': cls.GRID_COLOR,
                'linecolor': cls.AXIS_COLOR,
                'tickcolor': cls.AXIS_COLOR
            },
            'yaxis': {
                'gridcolor': cls.GRID_COLOR,
                'linecolor': cls.AXIS_COLOR,
                'tickcolor': cls.AXIS_COLOR
            }
        }
