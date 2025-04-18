import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# Configuration
VEGETABLES = ['potato', 'tomato', 'onion', 'garlic', 'cabbage', 'carrot']
MARKET_URL = 'https://www.marketwatch.com/investing/future/corn'  # Example - replace with actual vegetable market page

def scrape_market_prices():
    """
    Scrape vegetable prices from a market website
    """
    prices_data = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(MARKET_URL, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # This is a generic example - you'll need to inspect the actual website structure
        price_table = soup.find('table', {'class': 'prices-table'})  # Adjust class name
        
        if price_table:
            rows = price_table.find_all('tr')[1:]  # Skip header
            
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    veg_name = cols[0].text.strip().lower()
                    
                    if veg_name in VEGETABLES:
                        price_entry = {
                            'vegetable': veg_name,
                            'price': cols[1].text.strip(),
                            'unit': 'USD/kg',
                            'market': 'Online Market',
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        prices_data.append(price_entry)
        
    except Exception as e:
        print(f"Error during scraping: {str(e)}")
    
    # Save to CSV
    if prices_data:
        df = pd.DataFrame(prices_data)
        df.to_csv('scraped_vegetable_prices.csv', index=False)
        print("Scraped data saved to scraped_vegetable_prices.csv")
        return df
    else:
        print("No data scraped")
        return None

if __name__ == "__main__":
    scraped_df = scrape_market_prices()
    if scraped_df is not None:
        print(scraped_df)