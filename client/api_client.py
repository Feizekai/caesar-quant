import requests
import logging
import time
import pandas as pd

logger = logging.getLogger(__name__)

class APIClient:
    """External API client for fetching stock data"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
        
    def fetch_intraday_data(self, symbol, interval):
        """Fetch intraday data from Alpha Vantage API"""
        try:
            # Alpha Vantage API endpoint for intraday data
            params = {
                'function': 'TIME_SERIES_INTRADAY',
                'symbol': symbol,
                'interval': interval,
                'outputsize': 'full',
                'apikey': self.api_key,
                'datatype': 'json',
                'extended_hours': 'false'
            }
            
            # Make API request
            response = requests.get(self.base_url, params=params)
            
            # Check if request was successful
            if response.status_code != 200:
                logger.error(f"API request failed with status code {response.status_code}")
                return None
                
            # Log the raw response for debugging
            logger.debug(f"Raw API response: {response.text}")
            
            data = response.json()
            
            # Check if we got an error response
            if 'Error Message' in data:
                logger.error(f"Alpha Vantage API error: {data['Error Message']}")
                return None
                
            if 'Note' in data:
                logger.warning(f"Alpha Vantage API note: {data['Note']}")
                
            # Get the time series key
            time_series_key = None
            for key in data.keys():
                if key.startswith('Time Series'):
                    time_series_key = key
                    break
                    
            if not time_series_key:
                logger.error("Could not find time series data in API response")
                return None
                
            # Convert to DataFrame
            df = pd.DataFrame.from_dict(data[time_series_key], orient='index')
            
            # Convert index to datetime
            df.index = pd.to_datetime(df.index)
            
            # Set column names based on actual data
            # Alpha Vantage typically returns: open, high, low, close, volume
            if len(df.columns) >= 5:
                df.columns = ['open', 'high', 'low', 'close', 'volume']
                
                # Try to extract additional bid/ask data if available
                if len(df.columns) >= 9:
                    df.columns = ['open', 'high', 'low', 'close', 'volume', 'bid_price', 'ask_price', 'bid_size', 'ask_size']
            
            # Convert columns to numeric
            df = df.apply(pd.to_numeric, errors='coerce')
            
            # Sort by timestamp
            df = df.sort_index()
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching data from Alpha Vantage: {str(e)}", exc_info=True)
            return None
            
    def fetch_daily_data(self, symbol):
        """Fetch daily data from Alpha Vantage API"""
        try:
            # Alpha Vantage API endpoint for daily data
            params = {
                'function': 'TIME_SERIES_DAILY',
                'symbol': symbol,
                'outputsize': 'full',
                'apikey': self.api_key,
                'datatype': 'json'
            }
            
            # Make API request
            response = requests.get(self.base_url, params=params)
            
            # Check if request was successful
            if response.status_code != 200:
                logger.error(f"API request failed with status code {response.status_code}")
                return None
                
            # Log the raw response for debugging
            logger.debug(f"Raw API response: {response.text}")
            
            data = response.json()
            
            # Check if we got an error response
            if 'Error Message' in data:
                logger.error(f"Alpha Vantage API error: {data['Error Message']}")
                return None
                
            if 'Note' in data:
                logger.warning(f"Alpha Vantage API note: {data['Note']}")
                
            # Get the time series key
            time_series_key = None
            for key in data.keys():
                if key.startswith('Time Series'):
                    time_series_key = key
                    break
                    
            if not time_series_key:
                logger.error("Could not find time series data in API response")
                return None
                
            # Convert to DataFrame
            df = pd.DataFrame.from_dict(data[time_series_key], orient='index')
            
            # Convert index to datetime
            df.index = pd.to_datetime(df.index)
            
            # Set column names based on actual data
            # Alpha Vantage typically returns: open, high, low, close, volume
            if len(df.columns) >= 5:
                df.columns = ['open', 'high', 'low', 'close', 'volume']
            
            # Convert columns to numeric
            df = df.apply(pd.to_numeric, errors='coerce')
            
            # Sort by timestamp
            df = df.sort_index()
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching data from Alpha Vantage: {str(e)}", exc_info=True)
            return None