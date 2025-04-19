import requests
import pandas as pd
from datetime import datetime
from config import settings
from src.utils import log_message

class AgricultureAPI:
    def __init__(self):
        self.base_url = settings.AGRICULTURE_API_URL
        self.api_key = settings.AGRICULTURE_API_KEY
        
        import httpx
import asyncio
from datetime import datetime
from typing import List, Dict
from pydantic import BaseModel

class VegetablePrice(BaseModel):
    name: str
    price: float
    unit: str
    market: str
    timestamp: datetime
    currency: str = "EGP"  # Default to Egyptian Pound

class AgricultureAPI:
    def __init__(self, api_key: str):
        self.base_url = "https://api.agromonitoring.com/agro/1.0"
        self.api_key = api_key
        self.timeout = httpx.Timeout(10.0)

    async def fetch_prices(self, vegetables: List[str]) -> List[VegetablePrice]:
        """Fetch prices for multiple vegetables asynchronously"""
        async with httpx.AsyncClient() as client:
            tasks = [self._get_vegetable_price(client, veg) for veg in vegetables]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
        # Filter out errors and flatten results
        valid_prices = []
        for result in results:
            if isinstance(result, Exception):
                print(f"Error fetching prices: {result}")
                continue
            valid_prices.extend(result)
            
        return valid_prices

    async def _get_vegetable_price(self, client: httpx.AsyncClient, vegetable: str) -> List[VegetablePrice]:
        """Fetch prices for a single vegetable"""
        try:
            response = await client.get(
                f"{self.base_url}/market/prices",
                params={
                    "product": vegetable,
                    "appid": self.api_key,
                    "units": "metric"
                },
                timeout=self.timeout
            )
            response.raise_for_status()
            
            return [
                VegetablePrice(
                    name=vegetable,
                    price=item["price"],
                    unit=item.get("unit", "kg"),
                    market=item["market"],
                    timestamp=datetime.strptime(item["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
                )
                for item in response.json()["data"]
            ]
        except Exception as e:
            print(f"Error fetching {vegetable}: {str(e)}")
            return []

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