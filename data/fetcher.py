import pandas as pd
import os
import logging
import time
import sys
from datetime import datetime

# Add the project root directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config.reader import load_factors_config, get_minute_levels, load_symbols_config, get_symbols
from client.api_client import APIClient

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fetch_stock_data(symbol, api_key, output='./output'):
    """
    Fetch stock data for a given symbol from Alpha Vantage API and save to CSV files.
    """
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output):
            os.makedirs(output)
            logger.info(f"Created output directory: {output}")
        
        # Load factors configuration
        config = load_factors_config()
        if not config:
            logger.error("Failed to load factors configuration")
            return
        
        # Get minute levels from configuration
        minute_levels = get_minute_levels(config)
        if not minute_levels:
            logger.error("No minute levels found in configuration")
            return
        
        # Map minute levels to Alpha Vantage intervals
        interval_mapping = {
            '1_minute': '1min',
            '5_minute': '5min',
            '15_minute': '15min',
            '30_minute': '30min',
            '1_day': 'daily'
        }
        
        # Initialize API client
        api_client = APIClient(api_key)
        
        # Create symbol-specific directory
        symbol_output_dir = os.path.join(output, symbol)
        if not os.path.exists(symbol_output_dir):
            os.makedirs(symbol_output_dir)
            logger.info(f"Created symbol directory: {symbol_output_dir}")
        
        # Process each minute level
        for minute_level in minute_levels:
            if minute_level not in interval_mapping:
                logger.warning(f"Unknown minute level: {minute_level}")
                continue
                
            interval = interval_mapping[minute_level]
            logger.info(f"Fetching {minute_level} ({interval}) data for {symbol} from Alpha Vantage...")
            
            # Fetch data from Alpha Vantage
            if minute_level == '1_day':
                df = api_client.fetch_daily_data(symbol)
            else:
                df = api_client.fetch_intraday_data(symbol, interval)
            
            if df is None or df.empty:
                logger.warning(f"No data fetched for {minute_level} interval")
                continue
            
            # Save to CSV with simplified filename (without timestamp)
            filename = f"{symbol_output_dir}/{symbol}_{minute_level}.csv"
            df.to_csv(filename)
            logger.info(f"Saved {len(df)} rows to {filename}")
            
            # Add delay to respect API rate limits
            time.sleep(12)  # Alpha Vantage free tier: 5 requests per minute (12 seconds between requests)
            
        logger.info("Data fetching completed successfully")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        raise

def fetch_all_stocks_data(api_key, output='./output'):
    """Fetch stock data for all symbols in the configuration file."""
    try:
        # Load symbols configuration
        symbols_config = load_symbols_config()
        if not symbols_config:
            logger.error("Failed to load symbols configuration")
            return
        
        # Get symbols from configuration
        symbols = get_symbols(symbols_config)
        if not symbols:
            logger.error("No symbols found in configuration")
            return
        
        # Fetch data for each symbol
        for symbol in symbols:
            logger.info(f"Fetching data for symbol: {symbol}")
            fetch_stock_data(symbol, api_key, output)
            
        logger.info("Data fetching for all symbols completed successfully")
        
    except Exception as e:
        logger.error(f"An error occurred while fetching data for all symbols: {str(e)}", exc_info=True)
        raise