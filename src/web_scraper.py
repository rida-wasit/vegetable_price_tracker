
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .models import VegetablePrice  # Shared model from api_integration.py
import re
from typing import List

class MoroccoMarketScraper:
    BASE_URL = "https://www.villedesale.ma/%d8%a3%d8%ab%d9%85%d9%86%d8%a9-%d8%b3%d9%88%d9%82-%d8%a7%d9%84%d8%ac%d9%85%d9%84%d8%a9-%d8%a8%d8%b3%d9%84%d8%a7/"

    def scrape(self) -> List[VegetablePrice]:
        try:
            # Configure headers to mimic browser request
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
                "Accept-Encoding": "gzip, deflate, br"
            }
            
            response = requests.get(self.BASE_URL, headers=headers, timeout=15)
            response.raise_for_status()
            
            # Handle Arabic encoding
            response.encoding = 'utf-8'  
            soup = BeautifulSoup(response.text, 'html.parser')
            
            return self._parse_prices(soup)
            
        except Exception as e:
            print(f"Scraping failed: {str(e)}")
            return []

    def _parse_prices(self, soup: BeautifulSoup) -> List[VegetablePrice]:
        prices = []
        
        # Find the main content container (inspect the page to adjust this)
        content_div = soup.find('div', class_='entry-content')
        
        if not content_div:
            return prices
            
        # Extract all paragraphs containing price data
        for paragraph in content_div.find_all('p'):
            text = paragraph.get_text(strip=True)
            
            # Pattern for: "الطماطم: 4.50 درهم/كيلو" (Tomato: 4.50 DH/kg)
            match = re.search(r"(.+?):\s*([\d.]+)\s*درهم/(.+)", text)
            
            if match:
                veg_arabic = match.group(1).strip()
                price = float(match.group(2))
                unit = match.group(3).strip()
                
                prices.append(
                    VegetablePrice(
                        name=self._translate_vegetable(veg_arabic),
                        name_ar=veg_arabic,
                        price=price,
                        unit=self._standardize_unit(unit),
                        market="سوق الجملة سلا",
                        source="Ville de Sale",
                        currency="MAD",
                        timestamp=datetime.now()
                    )
                )
        return prices

    def _translate_vegetable(self, arabic_name: str) -> str:
        """Convert Arabic names to English standard"""
        translations = {
            "الطماطم": "tomato",
            "البطاطس": "potato",
            "البصل": "onion",
            "الثوم": "garlic",
            "الجزر": "carrot"
        }
        return translations.get(arabic_name, arabic_name)

    def _standardize_unit(self, unit: str) -> str:
        """Standardize Arabic/English units"""
        units_map = {
            "كيلو": "kilogram",
            "كلغ": "kilogram",
            "طن": "ton",
            "كجم": "kilogram"
        }
        return units_map.get(unit.lower(), unit)