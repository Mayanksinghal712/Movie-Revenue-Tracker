"""
Ultra-Modern Theme for Movie Revenue Tracker
Advanced Dark Mode with Neon Accents and Cinematic Design
"""

def load_ultra_modern_theme():
    """Load ultra-modern cinematic theme with neon accents"""
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&display=swap');
        
        /* === ULTRA-MODERN CSS VARIABLES === */
        :root {
            /* Cinematic Color Palette */
            --bg-primary: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
            --bg-secondary: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            --bg-tertiary: linear-gradient(135deg, #16213e 0%, #0f3460 50%, #533483 100%);
            
            /* Neon Accent Colors */
            --neon-cyan: #00d4ff;
            --neon-purple: #b24cf3;
            --neon-pink: #ff006e;
            --neon-green: #39ff14;
            --neon-orange: #ff8c00;
            --neon-blue: #1e90ff;
            
            /* Glass Morphism Advanced */
            --glass-ultra: rgba(255, 255, 255, 0.02);
            --glass-light: rgba(255, 255, 255, 0.05);
            --glass-medium: rgba(255, 255, 255, 0.08);
            --glass-strong: rgba(255, 255, 255, 0.12);
            --glass-border: rgba(0, 212, 255, 0.2);
            --glass-border-hover: rgba(0, 212, 255, 0.4);
            
            /* Typography Colors */
            --text-primary: #ffffff;
            --text-secondary: #e2e8f0;
            --text-tertiary: #cbd5e1;
            --text-muted: #94a3b8;
            --text-disabled: #64748b;
            --text-neon: var(--neon-cyan);
            --text-accent: var(--neon-purple);
            
            /* Advanced Shadows */
            --shadow-glow-cyan: 0 0 20px rgba(0, 212, 255, 0.3);
            --shadow-glow-purple: 0 0 20px rgba(178, 76, 243, 0.3);
            --shadow-glow-pink: 0 0 20px rgba(255, 0, 110, 0.3);
            --shadow-soft: 0 4px 24px rgba(0, 0, 0, 0.15);
            --shadow-medium: 0 8px 32px rgba(0, 0, 0, 0.25);
            --shadow-strong: 0 16px 48px rgba(0, 0, 0, 0.4);
            --shadow-cinema: 0 20px 60px rgba(0, 0, 0, 0.6);
            
            /* Advanced Animations */
            --transition-fast: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            --transition-smooth: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            --transition-slow: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            --transition-bounce: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            
            /* Modern Spacing */
            --space-xs: 0.25rem;
            --space-sm: 0.5rem;
            --space-md: 1rem;
            --space-lg: 1.5rem;
            --space-xl: 2rem;
            --space-2xl: 3rem;
            --space-3xl: 4rem;
            
            /* Border Radius */
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --radius-xl: 24px;
            --radius-2xl: 32px;
            --radius-full: 9999px;
        }
        
        /* === GLOBAL ULTRA-MODERN STYLES === */
        .stApp {
            background: var(--bg-primary);
            background-attachment: fixed;
            color: var(--text-primary);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.6;
            overflow-x: hidden;
        }
        
        .main .block-container {
            padding: var(--space-lg) var(--space-md);
            max-width: 1400px;
            margin: 0 auto;
        }
        
        /* Hide Streamlit Elements */
        #MainMenu { visibility: hidden !important; }
        footer { visibility: hidden !important; }
        header { visibility: hidden !important; }
        .stDeployButton { display: none !important; }
        
        /* === CINEMATIC TYPOGRAPHY === */
        .main-header {
            font-family: 'Orbitron', monospace;
            font-size: clamp(2.5rem, 8vw, 5rem);
            font-weight: 900;
            text-align: center;
            margin: var(--space-2xl) 0 var(--space-lg) 0;
            background: linear-gradient(135deg, var(--neon-cyan) 0%, var(--neon-purple) 50%, var(--neon-pink) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
            animation: headerPulse 4s ease-in-out infinite alternate,
                       textGlow 2s ease-in-out infinite alternate;
            letter-spacing: -0.02em;
            position: relative;
        }
        
        .main-header::before {
            content: '';
            position: absolute;
            top: -20px;
            left: -20px;
            right: -20px;
            bottom: -20px;
            background: radial-gradient(circle, rgba(0, 212, 255, 0.1) 0%, transparent 70%);
            border-radius: var(--radius-2xl);
            z-index: -1;
            animation: headerAura 3s ease-in-out infinite alternate;
        }
        
        @keyframes headerPulse {
            0% { transform: scale(1) translateY(0); }
            100% { transform: scale(1.02) translateY(-2px); }
        }
        
        @keyframes textGlow {
            0% { 
                text-shadow: 0 0 20px rgba(0, 212, 255, 0.3),
                           0 0 40px rgba(178, 76, 243, 0.2); 
            }
            100% { 
                text-shadow: 0 0 30px rgba(0, 212, 255, 0.6),
                           0 0 60px rgba(178, 76, 243, 0.4); 
            }
        }
        
        @keyframes headerAura {
            0% { opacity: 0.3; transform: scale(1); }
            100% { opacity: 0.6; transform: scale(1.1); }
        }
        
        .sub-header {
            font-family: 'Inter', sans-serif;
            font-size: clamp(1.1rem, 3vw, 1.5rem);
            font-weight: 400;
            text-align: center;
            color: var(--text-secondary);
            margin-bottom: var(--space-3xl);
            opacity: 0.9;
            letter-spacing: 0.5px;
            animation: fadeInUp 1s ease-out 0.3s both;
        }
        
        .analysis-header {
            font-family: 'Orbitron', monospace;
            font-size: clamp(1.8rem, 5vw, 2.8rem);
            font-weight: 700;
            text-align: center;
            margin: var(--space-2xl) 0 var(--space-xl) 0;
            background: linear-gradient(135deg, var(--neon-cyan) 0%, var(--neon-blue) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: var(--shadow-glow-cyan);
            animation: fadeInUp 0.8s ease-out;
            letter-spacing: -0.01em;
        }
        
        /* === ULTRA-MODERN METRIC CARDS === */
        .metric-card {
            background: var(--glass-medium);
            backdrop-filter: blur(24px) saturate(180%);
            border: 1px solid var(--glass-border);
            padding: var(--space-xl) var(--space-lg);
            border-radius: var(--radius-xl);
            color: var(--text-primary);
            text-align: center;
            box-shadow: var(--shadow-medium);
            transition: var(--transition-smooth);
            margin-bottom: var(--space-md);
            font-family: 'Inter', sans-serif;
            position: relative;
            overflow: hidden;
            cursor: pointer;
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, 
                transparent 0%, 
                rgba(0, 212, 255, 0.1) 50%, 
                transparent 100%);
            transition: left 0.8s ease;
        }
        
        .metric-card::after {
            content: '';
            position: absolute;
            inset: 0;
            border-radius: inherit;
            padding: 1px;
            background: linear-gradient(135deg, 
                var(--neon-cyan) 0%, 
                var(--neon-purple) 50%, 
                var(--neon-pink) 100%);
            mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            mask-composite: exclude;
            opacity: 0;
            transition: var(--transition-smooth);
        }
        
        .metric-card:hover {
            transform: translateY(-12px) scale(1.03);
            box-shadow: var(--shadow-strong), var(--shadow-glow-cyan);
            border-color: var(--glass-border-hover);
            background: var(--glass-strong);
        }
        
        .metric-card:hover::before {
            left: 100%;
        }
        
        .metric-card:hover::after {
            opacity: 1;
        }
        
        .metric-card h3 {
            font-size: clamp(2rem, 5vw, 3rem);
            margin-bottom: var(--space-md);
            color: var(--text-primary);
            filter: drop-shadow(0 0 15px rgba(0, 212, 255, 0.4));
            animation: cardFloat 4s ease-in-out infinite;
            font-weight: 600;
        }
        
        @keyframes cardFloat {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            25% { transform: translateY(-3px) rotate(0.5deg); }
            50% { transform: translateY(-6px) rotate(0deg); }
            75% { transform: translateY(-3px) rotate(-0.5deg); }
        }
        
        .metric-card h2 {
            font-family: 'JetBrains Mono', monospace;
            font-size: clamp(1.5rem, 4vw, 2.2rem);
            font-weight: 700;
            margin: var(--space-md) 0;
            background: linear-gradient(135deg, var(--neon-cyan) 0%, var(--neon-blue) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: var(--shadow-glow-cyan);
            letter-spacing: -0.02em;
        }
        
        .metric-card p {
            font-size: 0.875rem;
            font-weight: 500;
            color: var(--text-tertiary);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin: 0;
            opacity: 0.9;
        }
        
        /* === ADVANCED SIDEBAR === */
        .css-1d391kg {
            background: var(--glass-light) !important;
            backdrop-filter: blur(24px) saturate(180%);
            border-right: 1px solid var(--glass-border);
            box-shadow: var(--shadow-medium);
        }
        
        .css-1d391kg .css-1y4p8pa {
            background: transparent;
        }
        
        /* === ULTRA-MODERN FORM CONTROLS === */
        .stSelectbox label, .stSlider label, .stNumberInput label, .stRadio label {
            color: var(--text-primary) !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.95rem !important;
            margin-bottom: var(--space-sm) !important;
        }
        
        .stSelectbox > div > div {
            background: var(--glass-medium) !important;
            backdrop-filter: blur(16px);
            border: 1px solid var(--glass-border) !important;
            border-radius: var(--radius-lg) !important;
            color: var(--text-primary) !important;
            font-family: 'Inter', sans-serif;
            transition: var(--transition-smooth);
            box-shadow: var(--shadow-soft);
        }
        
        .stSelectbox > div > div:hover {
            border-color: var(--glass-border-hover) !important;
            box-shadow: var(--shadow-glow-cyan);
        }
        
        .stSelectbox > div > div > div {
            color: var(--text-primary) !important;
        }
        
        .stSlider > div > div > div {
            background: var(--glass-medium) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-soft);
        }
        
        .stNumberInput > div > div > input {
            background: var(--glass-medium) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: var(--radius-lg) !important;
            color: var(--text-primary) !important;
            font-family: 'JetBrains Mono', monospace !important;
            transition: var(--transition-smooth);
        }
        
        .stNumberInput > div > div > input:focus {
            border-color: var(--neon-cyan) !important;
            box-shadow: var(--shadow-glow-cyan) !important;
        }
        
        .stRadio > div {
            color: var(--text-primary) !important;
        }
        
        .stRadio > div > label > div {
            color: var(--text-primary) !important;
            font-weight: 500;
        }
        
        /* === FUTURISTIC TABS === */
        .stTabs [data-baseweb="tab-list"] {
            gap: var(--space-md);
            background: var(--glass-medium);
            backdrop-filter: blur(24px) saturate(180%);
            padding: var(--space-lg);
            border-radius: var(--radius-xl);
            border: 1px solid var(--glass-border);
            box-shadow: var(--shadow-medium);
            margin-bottom: var(--space-xl);
        }
        
        .stTabs [data-baseweb="tab"] {
            background: var(--glass-light) !important;
            color: var(--text-secondary) !important;
            border-radius: var(--radius-lg) !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            padding: var(--space-md) var(--space-xl) !important;
            border: 1px solid var(--glass-border) !important;
            transition: var(--transition-smooth) !important;
            position: relative;
            overflow: hidden;
        }
        
        .stTabs [data-baseweb="tab"]::before {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, var(--neon-cyan) 0%, var(--neon-purple) 100%);
            opacity: 0;
            transition: var(--transition-smooth);
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, var(--neon-cyan) 0%, var(--neon-blue) 100%) !important;
            color: var(--text-primary) !important;
            font-weight: 700 !important;
            transform: translateY(-2px);
            box-shadow: var(--shadow-glow-cyan);
            border-color: var(--neon-cyan) !important;
        }
        
        .stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
            background: var(--glass-strong) !important;
            border-color: var(--glass-border-hover) !important;
            transform: translateY(-1px);
            box-shadow: var(--shadow-medium);
        }
        
        /* === ENHANCED DATA TABLES === */
        .stDataFrame {
            background: var(--glass-medium) !important;
            border-radius: var(--radius-lg);
            overflow: hidden;
            box-shadow: var(--shadow-medium);
            border: 1px solid var(--glass-border);
        }
        
        .stDataFrame table {
            background: transparent !important;
            color: var(--text-primary) !important;
            font-family: 'Inter', sans-serif;
        }
        
        .stDataFrame th {
            background: var(--glass-strong) !important;
            color: var(--text-primary) !important;
            font-weight: 700;
            font-family: 'Inter', sans-serif;
            border-bottom: 2px solid var(--glass-border) !important;
            padding: var(--space-md) !important;
        }
        
        .stDataFrame td {
            background: var(--glass-light) !important;
            color: var(--text-secondary) !important;
            border-bottom: 1px solid var(--glass-border) !important;
            padding: var(--space-sm) var(--space-md) !important;
            transition: var(--transition-fast);
        }
        
        .stDataFrame tr:hover td {
            background: var(--glass-medium) !important;
        }
        
        /* === CINEMATIC CHART CONTAINERS === */
        .js-plotly-plot {
            border-radius: var(--radius-xl);
            overflow: hidden;
            box-shadow: var(--shadow-strong);
            border: 1px solid var(--glass-border);
            background: var(--glass-medium);
            backdrop-filter: blur(24px);
            transition: var(--transition-smooth);
        }
        
        .js-plotly-plot:hover {
            box-shadow: var(--shadow-cinema), var(--shadow-glow-cyan);
            transform: translateY(-4px);
        }
        
        /* === FUTURISTIC BUTTONS === */
        .stButton > button {
            background: linear-gradient(135deg, var(--neon-cyan) 0%, var(--neon-blue) 100%) !important;
            color: var(--text-primary) !important;
            border: none !important;
            border-radius: var(--radius-lg) !important;
            padding: var(--space-md) var(--space-xl) !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            transition: var(--transition-bounce) !important;
            box-shadow: var(--shadow-medium);
            text-transform: uppercase;
            letter-spacing: 1px;
            position: relative;
            overflow: hidden;
        }
        
        .stButton > button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.6s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: var(--shadow-glow-cyan), var(--shadow-strong);
        }
        
        .stButton > button:hover::before {
            left: 100%;
        }
        
        .stDownloadButton > button {
            background: linear-gradient(135deg, var(--neon-green) 0%, var(--neon-cyan) 100%) !important;
            color: var(--text-primary) !important;
            border: none !important;
            border-radius: var(--radius-lg) !important;
            padding: var(--space-md) var(--space-xl) !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            transition: var(--transition-bounce) !important;
            box-shadow: var(--shadow-medium);
        }
        
        /* === CONTENT CARDS === */
        .content-card {
            background: var(--glass-medium);
            backdrop-filter: blur(24px) saturate(180%);
            border: 1px solid var(--glass-border);
            padding: var(--space-xl);
            border-radius: var(--radius-xl);
            box-shadow: var(--shadow-medium);
            margin-bottom: var(--space-xl);
            font-family: 'Inter', sans-serif;
            color: var(--text-primary);
            transition: var(--transition-smooth);
            position: relative;
            overflow: hidden;
        }
        
        .content-card::before {
            content: '';
            position: absolute;
            inset: 0;
            border-radius: inherit;
            padding: 1px;
            background: linear-gradient(135deg, var(--neon-cyan), var(--neon-purple));
            mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            mask-composite: exclude;
            opacity: 0;
            transition: var(--transition-smooth);
        }
        
        .content-card:hover {
            transform: translateY(-6px);
            box-shadow: var(--shadow-strong), var(--shadow-glow-cyan);
        }
        
        .content-card:hover::before {
            opacity: 1;
        }
        
        /* === ADVANCED SCROLLBAR === */
        ::-webkit-scrollbar {
            width: 12px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--glass-light);
            border-radius: var(--radius-full);
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, var(--neon-cyan), var(--neon-purple));
            border-radius: var(--radius-full);
            border: 2px solid transparent;
            background-clip: content-box;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, var(--neon-purple), var(--neon-pink));
            background-clip: content-box;
        }
        
        /* === ADVANCED ANIMATIONS === */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(50px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        .animated-element {
            animation: fadeInUp 0.8s ease-out;
        }
        
        .loading {
            animation: pulse 1.5s ease-in-out infinite;
        }
        
        /* === RESPONSIVE DESIGN === */
        @media (max-width: 768px) {
            .main-header {
                font-size: 2.5rem;
                margin: var(--space-xl) 0 var(--space-md) 0;
            }
            
            .metric-card {
                padding: var(--space-lg) var(--space-md);
            }
            
            .analysis-header {
                font-size: 2rem;
            }
            
            .main .block-container {
                padding: var(--space-md) var(--space-sm);
            }
        }
        
        @media (max-width: 480px) {
            .main-header {
                font-size: 2rem;
            }
            
            .stTabs [data-baseweb="tab"] {
                padding: var(--space-sm) var(--space-md) !important;
                font-size: 0.875rem !important;
            }
        }
        
        /* === UTILITY CLASSES === */
        .text-neon {
            color: var(--neon-cyan);
            text-shadow: var(--shadow-glow-cyan);
        }
        
        .text-gradient {
            background: linear-gradient(135deg, var(--neon-cyan), var(--neon-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .glow-effect {
            box-shadow: var(--shadow-glow-cyan);
        }
        
        .hover-lift {
            transition: var(--transition-smooth);
        }
        
        .hover-lift:hover {
            transform: translateY(-4px);
        }
    </style>
    """
