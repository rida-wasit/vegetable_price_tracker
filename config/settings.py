import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# API Configuration
AGRICULTURE_API_KEY = os.getenv('AGRICULTURE_API_KEY', 'your_api_key')
AGRICULTURE_API_URL = "https://www.villedesale.ma/%d8%a3%d8%ab%d9%85%d9%86%d8%a9-%d8%b3%d9%88%d9%82-%d8%a7%d9%84%d8%ac%d9%85%d9%84%d8%a9-%d8%a8%d8%b3%d9%84%d8%a7/"

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'vegetable_prices',
    'user': 'postgres',
    'password': 'postgres',
    'port': '5432'
}

# Supported Vegetables
VEGETABLES = {
    'potato': ['بطاطس', 'potatoes', 'patates'],
    'tomato': ['طماطم', 'tomatoes', 'pomodoro'],
    'onion': ['بصل', 'onions', 'oignon'],
    'garlic': ['ثوم', 'garlic']
}

# Market Sources
MARKET_SOURCES = ['Cairo Market', 'Alexandria Market', 'Luxor Market']