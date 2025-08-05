def load_dark_mode_css():
    """Load enhanced dark mode CSS with better text visibility"""
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;500;600&display=swap');
        
        /* === DARK MODE CSS VARIABLES === */
        :root {
            /* Dark Background Gradients */
            --bg-primary: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            --bg-secondary: linear-gradient(135deg, #2d2d2d 0%, #3a3a3a 100%);
            --bg-accent: linear-gradient(135deg, #3a3a3a 0%, #4a4a4a 100%);
            
            /* Glass Morphism for Dark Mode */
            --glass-dark: rgba(255, 255, 255, 0.05);
            --glass-medium: rgba(255, 255, 255, 0.10);
            --glass-light: rgba(255, 255, 255, 0.15);
            --glass-border: rgba(255, 255, 255, 0.15);
            
            /* Enhanced Text Colors */
            --text-primary: #ffffff;
            --text-secondary: #e0e0e0;
            --text-muted: #b0b0b0;
            --text-disabled: #666666;
            --text-accent: #4facfe;
            --text-success: #43e97b;
            --text-warning: #ffa726;
            --text-danger: #ff6b6b;
            
            /* Accent Colors */
            --accent-primary: #4facfe;
            --accent-secondary: #00f2fe;
            --accent-success: #43e97b;
            --accent-warning: #ffa726;
            --accent-danger: #ff6b6b;
            --accent-info: #4ecdc4;
            
            /* Shadows for Dark Mode */
            --shadow-soft: 0 4px 20px rgba(0, 0, 0, 0.3);
            --shadow-medium: 0 8px 30px rgba(0, 0, 0, 0.4);
            --shadow-strong: 0 15px 50px rgba(0, 0, 0, 0.6);
            --shadow-glow: 0 0 20px rgba(79, 172, 254, 0.3);
            
            /* Border and Spacing */
            --border-radius: 16px;
            --border-radius-lg: 24px;
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            --spacing-xs: 0.5rem;
            --spacing-sm: 1rem;
            --spacing-md: 1.5rem;
            --spacing-lg: 2rem;
            --spacing-xl: 3rem;
        }
        
        /* === GLOBAL DARK MODE STYLES === */
        .stApp {
            background: var(--bg-primary);
            background-attachment: fixed;
            color: var(--text-primary);
            font-family: 'Poppins', sans-serif;
        }
        
        .main .block-container {
            padding-top: var(--spacing-sm);
            max-width: 1400px;
            background: transparent;
        }
        
        /* Hide Default Streamlit Elements */
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        header { visibility: hidden; }
        .stDeployButton { display: none; }
        
        /* === ENHANCED TYPOGRAPHY === */
        .main-header {
            text-align: center;
            color: var(--text-primary);
            font-size: 4rem;
            margin: var(--spacing-lg) 0;
            font-weight: 800;
            font-family: 'Poppins', sans-serif;
            text-shadow: 0 0 30px rgba(79, 172, 254, 0.5);
            animation: headerPulse 4s ease-in-out infinite alternate;
            letter-spacing: -2px;
        }
        
        @keyframes headerPulse {
            0% { 
                filter: drop-shadow(0 0 20px rgba(79, 172, 254, 0.3));
                transform: scale(1);
            }
            100% { 
                filter: drop-shadow(0 0 40px rgba(79, 172, 254, 0.6));
                transform: scale(1.02);
            }
        }
        
        .sub-header {
            text-align: center;
            color: var(--text-secondary);
            font-size: 1.4rem;
            margin-bottom: var(--spacing-xl);
            font-weight: 400;
            font-family: 'Poppins', sans-serif;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
            letter-spacing: 0.5px;
        }
        
        .analysis-header {
            color: var(--text-accent);
            font-size: 2.5rem;
            font-weight: 700;
            margin: var(--spacing-lg) 0;
            font-family: 'Poppins', sans-serif;
            text-align: center;
            text-shadow: 0 0 20px rgba(79, 172, 254, 0.4);
            letter-spacing: -1px;
        }
        
        /* === ENHANCED METRIC CARDS === */
        .metric-card {
            background: var(--glass-medium);
            backdrop-filter: blur(20px) saturate(180%);
            border: 1px solid var(--glass-border);
            padding: var(--spacing-lg) var(--spacing-md);
            border-radius: var(--border-radius-lg);
            color: var(--text-primary);
            text-align: center;
            box-shadow: var(--shadow-medium);
            transition: var(--transition);
            margin-bottom: var(--spacing-sm);
            font-family: 'Poppins', sans-serif;
            position: relative;
            overflow: hidden;
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, var(--glass-light), transparent);
            transition: left 0.6s ease;
        }
        
        .metric-card:hover::before {
            left: 100%;
        }
        
        .metric-card:hover {
            transform: translateY(-8px) scale(1.03);
            box-shadow: var(--shadow-strong);
            border-color: var(--accent-primary);
            background: var(--glass-light);
        }
        
        .metric-card h3 {
            font-size: 2.5rem;
            margin-bottom: var(--spacing-sm);
            color: var(--text-primary);
            filter: drop-shadow(0 0 15px rgba(79, 172, 254, 0.4));
            animation: cardFloat 3s ease-in-out infinite;
        }
        
        @keyframes cardFloat {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-3px); }
        }
        
        .metric-card h2 {
            font-size: 2rem;
            margin: var(--spacing-sm) 0;
            font-weight: 700;
            color: var(--accent-primary);
            text-shadow: 0 0 15px rgba(79, 172, 254, 0.5);
            font-family: 'Roboto Mono', monospace;
        }
        
        .metric-card p {
            font-size: 0.9rem;
            margin: 0;
            color: var(--text-secondary);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            opacity: 0.9;
        }
        
        /* === ENHANCED SIDEBAR === */
        .css-1d391kg {
            background: var(--glass-dark) !important;
            backdrop-filter: blur(20px);
            border-right: 1px solid var(--glass-border);
        }
        
        .css-1d391kg .css-1y4p8pa {
            background: transparent;
        }
        
        /* === FORM CONTROLS DARK MODE === */
        .stSelectbox label, .stSlider label, .stNumberInput label, .stRadio label {
            color: var(--text-primary) !important;
            font-weight: 600 !important;
            font-family: 'Poppins', sans-serif !important;
            font-size: 1rem !important;
        }
        
        .stSelectbox > div > div {
            background: var(--glass-medium) !important;
            backdrop-filter: blur(10px);
            border: 1px solid var(--glass-border) !important;
            border-radius: var(--border-radius) !important;
            color: var(--text-primary) !important;
            font-family: 'Poppins', sans-serif;
        }
        
        .stSelectbox > div > div > div {
            color: var(--text-primary) !important;
        }
        
        .stSlider > div > div > div {
            background: var(--glass-medium) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: var(--border-radius);
        }
        
        .stNumberInput > div > div > input {
            background: var(--glass-medium) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: var(--border-radius) !important;
            color: var(--text-primary) !important;
        }
        
        .stRadio > div {
            color: var(--text-primary) !important;
        }
        
        .stRadio > div > label > div {
            color: var(--text-primary) !important;
        }
        
        /* === ENHANCED TABS === */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            background: var(--glass-medium);
            backdrop-filter: blur(20px);
            padding: var(--spacing-md);
            border-radius: var(--border-radius-lg);
            border: 1px solid var(--glass-border);
            box-shadow: var(--shadow-soft);
        }
        
        .stTabs [data-baseweb="tab"] {
            background: var(--glass-dark) !important;
            color: var(--text-secondary) !important;
            border-radius: var(--border-radius) !important;
            font-weight: 600 !important;
            font-family: 'Poppins', sans-serif !important;
            padding: var(--spacing-sm) var(--spacing-lg) !important;
            border: 1px solid var(--glass-border) !important;
            transition: var(--transition) !important;
        }
        
        .stTabs [aria-selected="true"] {
            background: var(--accent-primary) !important;
            color: var(--text-primary) !important;
            font-weight: 700 !important;
            transform: translateY(-2px);
            box-shadow: var(--shadow-glow);
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: var(--glass-medium) !important;
            border-color: var(--accent-primary) !important;
        }
        
        /* === TEXT VISIBILITY FIXES === */
        .stMarkdown p, .stMarkdown div, .stText {
            color: var(--text-primary) !important;
            font-family: 'Poppins', sans-serif;
        }
        
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, 
        .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
            color: var(--text-primary) !important;
            font-family: 'Poppins', sans-serif;
        }
        
        .stDataFrame {
            background: var(--glass-medium) !important;
            border-radius: var(--border-radius);
            overflow: hidden;
            box-shadow: var(--shadow-soft);
        }
        
        .stDataFrame table {
            background: transparent !important;
            color: var(--text-primary) !important;
        }
        
        .stDataFrame th {
            background: var(--glass-light) !important;
            color: var(--text-primary) !important;
            font-weight: 600;
            border-bottom: 1px solid var(--glass-border) !important;
        }
        
        .stDataFrame td {
            background: var(--glass-dark) !important;
            color: var(--text-secondary) !important;
            border-bottom: 1px solid var(--glass-border) !important;
        }
        
        /* === CHART CONTAINERS === */
        .js-plotly-plot {
            border-radius: var(--border-radius-lg);
            overflow: hidden;
            box-shadow: var(--shadow-medium);
            border: 1px solid var(--glass-border);
            background: var(--glass-medium);
            backdrop-filter: blur(20px);
        }
        
        /* === ENHANCED BUTTONS === */
        .stButton > button {
            background: var(--accent-primary) !important;
            color: var(--text-primary) !important;
            border: none !important;
            border-radius: var(--border-radius) !important;
            padding: var(--spacing-sm) var(--spacing-lg) !important;
            font-weight: 600 !important;
            font-family: 'Poppins', sans-serif !important;
            transition: var(--transition) !important;
            box-shadow: var(--shadow-soft);
        }
        
        .stButton > button:hover {
            background: var(--accent-secondary) !important;
            transform: translateY(-2px);
            box-shadow: var(--shadow-glow);
        }
        
        .stDownloadButton > button {
            background: var(--accent-success) !important;
            color: var(--text-primary) !important;
            border: none !important;
            border-radius: var(--border-radius) !important;
            padding: var(--spacing-sm) var(--spacing-lg) !important;
            font-weight: 600 !important;
            font-family: 'Poppins', sans-serif !important;
            transition: var(--transition) !important;
        }
        
        /* === CONTENT CARDS === */
        .content-card {
            background: var(--glass-medium);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            padding: var(--spacing-lg);
            border-radius: var(--border-radius-lg);
            box-shadow: var(--shadow-medium);
            margin-bottom: var(--spacing-lg);
            font-family: 'Poppins', sans-serif;
            color: var(--text-primary);
            transition: var(--transition);
        }
        
        .content-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-strong);
            border-color: var(--accent-primary);
        }
        
        /* === SCROLLBAR DARK MODE === */
        ::-webkit-scrollbar {
            width: 12px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--glass-dark);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--accent-primary);
            border-radius: 10px;
            border: 2px solid transparent;
            background-clip: content-box;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent-secondary);
            background-clip: content-box;
        }
        
        /* === RESPONSIVE DESIGN === */
        @media (max-width: 768px) {
            .main-header {
                font-size: 2.5rem;
            }
            
            .metric-card {
                padding: var(--spacing-md) var(--spacing-sm);
            }
            
            .analysis-header {
                font-size: 2rem;
            }
        }
        
        /* === LOADING ANIMATIONS === */
        @keyframes shimmer {
            0% { opacity: 0.6; }
            50% { opacity: 1; }
            100% { opacity: 0.6; }
        }
        
        .loading {
            animation: shimmer 1.5s ease-in-out infinite;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .animated-element {
            animation: slideUp 0.8s ease-out;
        }
        
        /* === SUCCESS INDICATORS === */
        .success-indicator {
            color: var(--accent-success);
            font-weight: 600;
        }
        
        .warning-indicator {
            color: var(--accent-warning);
            font-weight: 600;
        }
        
        .danger-indicator {
            color: var(--accent-danger);
            font-weight: 600;
        }
    </style>
    """
