"""RSI indicator calculation module"""
import pandas as pd
import numpy as np
import os
import logging
import matplotlib.pyplot as plt

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def calculate_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """
    Calculate RSI indicator for given stock data.
    
    Args:
        df: DataFrame with stock data containing 'close' column
        period: Period for RSI calculation (default: 14)
    
    Returns:
        DataFrame with RSI values
    """
    try:
        # Calculate price changes
        delta = df['close'].diff()
        
        # Separate gains and losses
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        # Calculate average gains and losses
        avg_gain = gain.rolling(window=period, min_periods=1).mean()
        avg_loss = loss.rolling(window=period, min_periods=1).mean()
        
        # Calculate RS and RSI
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        # Create result DataFrame
        result = pd.DataFrame({
            'RSI': rsi
        })
        
        return result
    except Exception as e:
        logger.error(f"Error calculating RSI: {str(e)}", exc_info=True)
        raise

def plot_rsi(df: pd.DataFrame, rsi_df: pd.DataFrame, symbol: str, time_level: str, output_dir: str) -> None:
    """
    Plot RSI indicator and save to file.
    
    Args:
        df: Original stock data DataFrame
        rsi_df: DataFrame with RSI values
        symbol: Stock symbol
        time_level: Time level (e.g., '1_minute', '5_minute', '1_day')
        output_dir: Output directory for plots
    """
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"Created output directory: {output_dir}")
        
        # Create the plot
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
        
        # Plot price data
        ax1.plot(df.index, df['close'], label='Close Price', color='black')
        ax1.set_title(f'{symbol} - Price Chart')
        ax1.set_ylabel('Price')
        ax1.legend()
        ax1.grid(True)
        
        # Plot RSI
        ax2.plot(rsi_df.index, rsi_df['RSI'], label='RSI', color='purple')
        
        # Add overbought and oversold lines
        ax2.axhline(y=70, color='r', linestyle='--', alpha=0.7, label='Overbought (70)')
        ax2.axhline(y=30, color='g', linestyle='--', alpha=0.7, label='Oversold (30)')
        ax2.axhline(y=50, color='gray', linestyle='-', alpha=0.5)
        
        ax2.set_title(f'{symbol} - RSI Indicator')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('RSI')
        ax2.set_ylim(0, 100)
        ax2.legend()
        ax2.grid(True)
        
        # Save plot
        plot_filename = os.path.join(output_dir, f'{symbol}_{time_level}_rsi.png')
        plt.tight_layout()
        plt.savefig(plot_filename)
        plt.close()
        
        logger.info(f"Saved RSI plot to {plot_filename}")
    except Exception as e:
        logger.error(f"Error plotting RSI: {str(e)}", exc_info=True)
        raise

def calculate_and_save_rsi(symbol: str, time_level: str, data_dir: str = './output', output_dir: str = './output') -> None:
    """
    Calculate RSI for given symbol and time level, save results to CSV and plot.
    
    Args:
        symbol: Stock symbol
        time_level: Time level (e.g., '1_minute', '5_minute', '1_day')
        data_dir: Directory containing stock data CSV files
        output_dir: Base output directory for RSI results
    """
    try:
        # Create symbol-specific output directory with time level
        symbol_output_dir = os.path.join(output_dir, symbol, 'indicators', 'rsi', time_level)
        
        # Read stock data
        data_file = os.path.join(data_dir, symbol, f'{symbol}_{time_level}.csv')
        if not os.path.exists(data_file):
            logger.warning(f"Data file not found: {data_file}")
            return
        
        df = pd.read_csv(data_file)
        
        # Convert timestamp column to datetime if it exists
        timestamp_cols = [col for col in df.columns if 'time' in col.lower() or 'date' in col.lower()]
        if timestamp_cols:
            df[timestamp_cols[0]] = pd.to_datetime(df[timestamp_cols[0]])
            df.set_index(timestamp_cols[0], inplace=True)
        
        # Calculate RSI
        rsi_df = calculate_rsi(df)
        
        # Save RSI to CSV
        if not os.path.exists(symbol_output_dir):
            os.makedirs(symbol_output_dir)
            logger.info(f"Created symbol directory: {symbol_output_dir}")
        
        csv_filename = os.path.join(symbol_output_dir, f'{symbol}_{time_level}_rsi.csv')
        
        # Check if CSV file already exists
        if os.path.exists(csv_filename):
            logger.info(f"RSI data already exists for {symbol} {time_level}, skipping calculation")
            return
        
        rsi_df.to_csv(csv_filename)
        logger.info(f"Saved RSI data to {csv_filename}")
        
        # Plot RSI
        plot_rsi(df, rsi_df, symbol, time_level, symbol_output_dir)
        
    except Exception as e:
        logger.error(f"Error calculating and saving RSI for {symbol} {time_level}: {str(e)}", exc_info=True)
        raise