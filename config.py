# API Configuration
COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"
TOKEN_ID = "kaito"
VS_CURRENCY = "usd"

# Analysis Parameters
DEFAULT_DAYS = 30
PRICE_SPIKE_THRESHOLD = 10.0  # percentage
VOLUME_SPIKE_THRESHOLD = 50.0  # percentage

# Output Paths
DATA_DIR = "./data"
REPORTS_DIR = "./reports"
VISUALIZATIONS_DIR = "./visualizations"

# Request Headers
HEADERS = {
    'Accept': 'application/json',
    'User-Agent': 'KAITO-Market-Tracker/1.0'
}

# Visualization Settings
FIGURE_SIZE = (14, 12)
DPI = 300
CHART_STYLE = 'seaborn-v0_8-darkgrid'