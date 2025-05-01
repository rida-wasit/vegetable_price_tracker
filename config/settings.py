import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# API Configuration
AGRICULTURE_API_KEY = os.getenv('AGRICULTURE_API_KEY', 'your_api_key')
AGRICULTURE_API_URL = "https://api.agromonitoring.com/agro/1.0"

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