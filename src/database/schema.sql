-- Table for vegetable prices
CREATE TABLE IF NOT EXISTS market_prices (
    id SERIAL PRIMARY KEY,
    vegetable VARCHAR(50) NOT NULL,
    vegetable_ar VARCHAR(50), -- Arabic name
    price NUMERIC(10,2) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    market VARCHAR(100) NOT NULL,
    source VARCHAR(50) NOT NULL,
    currency VARCHAR(3) DEFAULT 'EGP',
    timestamp TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (vegetable, market, timestamp)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_vegetable ON market_prices(vegetable);
CREATE INDEX IF NOT EXISTS idx_market ON market_prices(market);
CREATE INDEX IF NOT EXISTS idx_timestamp ON market_prices(timestamp);