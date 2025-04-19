import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_batch
from typing import List, Optional
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseHandler:
    def __init__(self):
        self.conn = self._connect()
        self._initialize_db()

    def _connect(self):
        return psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'vegetable_prices'),
            user=os.getenv('DB_USER', 'vegtracker'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT', '5432')
        )

    def _initialize_db(self):
        """Create tables if they don't exist"""
        with open('src/database/schema.sql') as f:
            schema = f.read()
        
        with self.conn.cursor() as cur:
            cur.execute(schema)
        self.conn.commit()

    def insert_prices(self, prices: List[dict]):
        """Bulk insert vegetable prices"""
        query = sql.SQL("""
            INSERT INTO market_prices (
                vegetable, vegetable_ar, price, unit, 
                market, source, currency, timestamp
            ) VALUES %s
            ON CONFLICT (vegetable, market, timestamp) 
            DO UPDATE SET 
                price = EXCLUDED.price,
                unit = EXCLUDED.unit
        """)
        
        data = [(
            p['name'],
            p.get('name_ar'),
            p['price'],
            p['unit'],
            p['market'],
            p['source'],
            p.get('currency', 'EGP'),
            p['timestamp']
        ) for p in prices]

        with self.conn.cursor() as cur:
            execute_batch(cur, query, data)
        self.conn.commit()

    def get_latest_prices(self, vegetable: str, limit: int = 10) -> List[dict]:
        """Retrieve latest prices for a vegetable"""
        query = """
            SELECT vegetable, price, unit, market, timestamp 
            FROM market_prices 
            WHERE vegetable = %s OR vegetable_ar = %s
            ORDER BY timestamp DESC 
            LIMIT %s
        """
        
        with self.conn.cursor() as cur:
            cur.execute(query, (vegetable, vegetable, limit))
            return [dict(row) for row in cur.fetchall()]

    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()