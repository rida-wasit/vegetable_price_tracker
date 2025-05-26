import psycopg2
import pandas as pd
from config import settings
from src.utils import log_message

class DataProcessor:
    def __init__(self):
        self.conn = self._connect_db()
        self._setup_database()

    def _connect_db(self):
        """Establish PostgreSQL connection"""
        try:
            return psycopg2.connect(**settings.DB_CONFIG)
        except Exception as e:
            log_message(f"DB Connection Error: {str(e)}", level='error')
            raise

    def _setup_database(self):
        """Initialize database tables"""
        with open(BASE_DIR / 'data/sql/setup.sql') as f:
            sql = f.read()
        
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
        self.conn.commit()

    def normalize_data(self, df):
        """Clean and standardize price data"""
        # Standardize vegetable names
        reverse_mapping = {}
        for std_name, variants in settings.VEGETABLES.items():
            for variant in variants:
                reverse_mapping[variant.lower()] = std_name
        
        df['vegetable'] = df['vegetable'].str.lower().map(reverse_mapping)
        
        # Clean price values
        df['price'] = pd.to_numeric(
            df['price'].astype(str).str.replace('[^\d.]', '', regex=True),
            errors='coerce'
        )
        
        # Standardize units
        df['unit'] = df['unit'].replace({
            'kg': 'kilogram',
            'kilo': 'kilogram',
            'طن': 'ton',
            'tonne': 'ton'
        })
        
        return df.dropna(subset=['price', 'vegetable'])

    def save_to_db(self, df):
        """Store processed data in PostgreSQL"""
        sql = """
        INSERT INTO market_prices 
        (vegetable, price, unit, market, source, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (vegetable, market, timestamp) 
        DO UPDATE SET price = EXCLUDED.price
        """
        
        with self.conn.cursor() as cursor:
            cursor.executemany(sql, df.to_records(index=False))
        self.conn.commit()
        log_message(f"Saved {len(df)} records to database")