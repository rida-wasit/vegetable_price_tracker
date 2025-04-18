import requests
import pandas as pd
from datetime import datetime
from config import settings
from src.utils import log_message

class AgricultureAPI:
    def __init__(self):
        self.base_url = settings.AGRICULTURE_API_URL
        self.api_key = settings.AGRICULTURE_API_KEY

    def get_vegetable_prices(self):
        """Fetch real-time prices from agriculture API"""
        try:
            params = {
                'appid': self.api_key,
                'products': ','.join(settings.VEGETABLES.keys())
            }
            
            response = requests.get(
                f"{self.base_url}/market/prices",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            prices = []
            for item in response.json().get('data', []):
                prices.append({
                    'vegetable': item['product'],
                    'price': item['price'],
                    'unit': item.get('unit', 'kg'),
                    'market': item['market'],
                    'source': 'AgricultureAPI',
                    'timestamp': datetime.strptime(item['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
                })
            
            return pd.DataFrame(prices)
            
        except Exception as e:
            log_message(f"API Error: {str(e)}", level='error')
            return pd.DataFrame()