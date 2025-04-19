from datetime import datetime
from src.database.db_handler import DatabaseHandler

class AgricultureAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.db = DatabaseHandler()

    async def fetch_and_store_prices(self, vegetables: List[str]):
        """Fetch prices and store in database"""
        prices = await self.fetch_prices_async(vegetables)
        if prices:
            self.db.insert_prices([price.dict() for price in prices])
            print(f"Inserted {len(prices)} records")