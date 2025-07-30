import click
import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from data.fetcher import fetch_stock_data

@click.command()
@click.option('--symbol', required=True, help='Stock symbol to fetch data for')
@click.option('--api-key', required=True, envvar='ALPHA_VANTAGE_API_KEY', 
              help='Alpha Vantage API key (can also be set via ALPHA_VANTAGE_API_KEY environment variable)')
@click.option('--output', default='./output', help='Output directory for CSV files')
def fetch_stock_data_command(symbol, api_key, output):
    """
    Fetch stock data for a given symbol from Alpha Vantage API and save to CSV files.
    """
    fetch_stock_data(symbol, api_key, output)

if __name__ == '__main__':
    fetch_stock_data_command()