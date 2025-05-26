import psycopg2
from datetime import datetime, timedelta
from config import settings
from src.utils import log_message

class VegetableChatbot:
    def __init__(self):
        self.db_conn = psycopg2.connect(**settings.DB_CONFIG)

    def get_current_prices(self, vegetable, market=None):
        """Query database for current prices"""
        try:
            # Get prices from last 24 hours
            cutoff = datetime.now() - timedelta(hours=24)
            
            query = """
            SELECT vegetable, price, unit, market, timestamp 
            FROM market_prices 
            WHERE vegetable = %s AND timestamp >= %s
            """
            params = [vegetable, cutoff]
            
            if market:
                query += " AND market = %s"
                params.append(market)
            
            query += " ORDER BY timestamp DESC LIMIT 1"
            
            with self.db_conn.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchone()
            
            if result:
                return self._format_response(*result)
            return "Sorry, no recent price data available."
            
        except Exception as e:
            log_message(f"Chatbot Error: {str(e)}", level='error')
            return "Sorry, I encountered an error fetching prices."

    def _format_response(self, vegetable, price, unit, market, timestamp):
        """Format price response for chatbot"""
        return (
            f"Current price for {vegetable} at {market}:\n"
            f"• Price: {price:.2f} EGP per {unit}\n"
            f"• Last updated: {timestamp.strftime('%Y-%m-%d %H:%M')}\n"
            f"• Source: Agricultural Market API"
        )