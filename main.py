from src.api_integration import AgricultureAPI
from src.data_processor import DataProcessor
from src.chatbot import VegetableChatbot
from src.utils import log_message
import schedule
import time

def update_prices():
    """Scheduled job to update prices"""
    log_message("Starting price update...")
    try:
        # Fetch data
        api = AgricultureAPI()
        raw_data = api.get_vegetable_prices()
        
        # Process and store
        processor = DataProcessor()
        clean_data = processor.normalize_data(raw_data)
        processor.save_to_db(clean_data)
        
        log_message("Price update completed successfully")
    except Exception as e:
        log_message(f"Update failed: {str(e)}", level='error')

def chatbot_interaction():
    """Simulate chatbot interaction"""
    chatbot = VegetableChatbot()
    while True:
        print("\nWhich vegetable price would you like to check?")
        veg = input("Enter vegetable name (or 'quit' to exit): ").strip().lower()
        
        if veg == 'quit':
            break
            
        market = input("Enter market name (optional): ").strip() or None
        print(chatbot.get_current_prices(veg, market))

if __name__ == "__main__":
    # Schedule hourly price updates
    schedule.every().hour.do(update_prices)
    
    # Initial update
    update_prices()
    
    # Start chatbot interface
    print("Vegetable Price Chatbot System")
    print("-----------------------------")
    chatbot_interaction()