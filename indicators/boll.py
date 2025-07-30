"""BOLL indicator calculation module"""
import pandas as pd
import numpy as np
import os
import logging
import matplotlib.pyplot as plt

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def calculate_boll(df: pd.DataFrame, period: int = 20, std_multiplier: float = 2.0) -> pd.DataFrame:
    """
    Calculate BOLL indicator for given stock data.
    
    Args:
        df: DataFrame with stock data containing 'close' column
        period: Period for moving average (default: 20)
        std_multiplier: Standard deviation multiplier for bands (default: 2.0)
    
    Returns:
        DataFrame with BOLL values (Middle, Upper, Lower)
    """
    try:
        # Calculate middle band (moving average)
        middle_band = df['close'].rolling(window=period).mean()
        
        # Calculate standard deviation
        std_dev = df['close'].rolling(window=period).std()
        
        # Calculate upper and lower bands
        upper_band = middle_band + (std_dev * std_multiplier)
        lower_band = middle_band - (std_dev * std_multiplier)
        
        # Create result DataFrame
        result = pd.DataFrame({
            'MIDDLE': middle_band,  # Middle band (MA)
            'UPPER': upper_band,    # Upper band
            'LOWER': lower_band     # Lower band
        })
        
        return result
    except Exception as e:
        logger.error(f"Error calculating BOLL: {str(e)}", exc_info=True)
        raise

def plot_boll(df: pd.DataFrame, boll_df: pd.DataFrame, symbol: str, time_level: str, output_dir: str) -> None:
    """
    Plot BOLL indicator and save to file.
    
    Args:
        df: Original stock data DataFrame
        boll_df: DataFrame with BOLL values
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
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Plot price data
        ax.plot(df.index, df['close'], label='Close Price', color='black')
        
        # Plot BOLL bands
        ax.plot(boll_df.index, boll_df['MIDDLE'], label='Middle Band', color='blue')
        ax.plot(boll_df.index, boll_df['UPPER'], label='Upper Band', color='red', linestyle='--')
        ax.plot(boll_df.index, boll_df['LOWER'], label='Lower Band', color='green', linestyle='--')
        
        # Fill area between bands
        ax.fill_between(boll_df.index, boll_df['UPPER'], boll_df['LOWER'], color='gray', alpha=0.1)
        
        ax.set_title(f'{symbol} - BOLL Indicator')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend()
        ax.grid(True)
        
        # Save plot
        plot_filename = os.path.join(output_dir, f'{symbol}_{time_level}_boll.png')
        plt.tight_layout()
        plt.savefig(plot_filename)
        plt.close()
        
        logger.info(f"Saved BOLL plot to {plot_filename}")
    except Exception as e:
        logger.error(f"Error plotting BOLL: {str(e)}", exc_info=True)
        raise

def calculate_and_save_boll(symbol: str, time_level: str, data_dir: str = './output', output_dir: str = './output') -> None:
    """
    Calculate BOLL for given symbol and time level, save results to CSV and plot.
    
    Args:
        symbol: Stock symbol
        time_level: Time level (e.g., '1_minute', '5_minute', '1_day')
        data_dir: Directory containing stock data CSV files
        output_dir: Base output directory for BOLL results
    """
    try:
        # Create symbol-specific output directory with time level
        symbol_output_dir = os.path.join(output_dir, symbol, 'indicators', 'boll', time_level)
        
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
        
        # Calculate BOLL
        boll_df = calculate_boll(df)
        
        # Save BOLL to CSV
        if not os.path.exists(symbol_output_dir):
            os.makedirs(symbol_output_dir)
            logger.info(f"Created symbol directory: {symbol_output_dir}")
        
        csv_filename = os.path.join(symbol_output_dir, f'{symbol}_{time_level}_boll.csv')
        
        # Check if CSV file already exists
        if os.path.exists(csv_filename):
            logger.info(f"BOLL data already exists for {symbol} {time_level}, skipping calculation")
            return
        
        boll_df.to_csv(csv_filename)
        logger.info(f"Saved BOLL data to {csv_filename}")
        
        # Plot BOLL
        plot_boll(df, boll_df, symbol, time_level, symbol_output_dir)
        
    except Exception as e:
        logger.error(f"Error calculating and saving BOLL for {symbol} {time_level}: {str(e)}", exc_info=True)
        raise