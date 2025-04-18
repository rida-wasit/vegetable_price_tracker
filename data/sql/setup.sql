-- vegetable_price_tracker/data/sql/setup.sql

-- Enable Unicode and Arabic text support
CREATE EXTENSION IF NOT EXISTS "unaccent";

-- Create market prices table
CREATE TABLE IF NOT EXISTS market_prices (
    id SERIAL PRIMARY KEY,
    vegetable VARCHAR(50) NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    market VARCHAR(100) NOT NULL,
    source VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    UNIQUE (vegetable, market, timestamp)
);

-- Create indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_market_prices_vegetable ON market_prices(vegetable);
CREATE INDEX IF NOT EXISTS idx_market_prices_timestamp ON market_prices(timestamp);
CREATE INDEX IF NOT EXISTS idx_market_prices_market ON market_prices(market);

-- Create view for Arabic vegetable names
CREATE OR REPLACE VIEW arabic_vegetable_prices AS
SELECT 
    CASE
        WHEN vegetable = 'potato' THEN 'بطاطس'
        WHEN vegetable = 'tomato' THEN 'طماطم'
        WHEN vegetable = 'onion' THEN 'بصل'
        WHEN vegetable = 'garlic' THEN 'ثوم'
        ELSE vegetable
    END AS vegetable_arabic,
    price,
    CASE
        WHEN unit = 'kilogram' THEN 'كيلوغرام'
        WHEN unit = 'ton' THEN 'طن'
        ELSE unit
    END AS unit_arabic,
    market,
    timestamp
FROM market_prices;

-- Insert sample data (optional)
INSERT INTO market_prices (vegetable, price, unit, market, source, timestamp)
VALUES 
    ('potato', 12.50, 'kilogram', 'Cairo Market', 'API', NOW() - INTERVAL '2 hours'),
    ('tomato', 8.75, 'kilogram', 'Alexandria Market', 'Scraping', NOW() - INTERVAL '1 hour'),
    ('onion', 5.25, 'kilogram', 'Luxor Market', 'API', NOW() - INTERVAL '3 hours')
ON CONFLICT (vegetable, market, timestamp) DO NOTHING;