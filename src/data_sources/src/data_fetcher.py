from .database.db_handler import DatabaseHandler

class VegetablePriceFetcher:
    def __init__(self):
        self.db = DatabaseHandler()
        
    async def fetch_and_store(self):
        prices = await self._fetch_from_sources()
        self.db.insert_prices([price.to_dict() for price in prices])
        
    async def get_prices(self, vegetable: str) -> List[Dict]:
        return self.db.get_latest_prices(vegetable)