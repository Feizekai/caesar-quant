"""MACD indicator calculation module"""
import pandas as pd
import numpy as np
import os
import logging
import matplotlib.pyplot as plt
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def calculate_macd(df: pd.DataFrame, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> pd.DataFrame:
    """
    Calculate MACD indicator for given stock data.
    
    Args:
        df: DataFrame with stock data containing 'close' column
        fast_period: Fast EMA period (default: 12)
        slow_period: Slow EMA period (default: 26)
        signal_period: Signal line EMA period (default: 9)
    
    Returns:
        DataFrame with MACD values (MACD, Signal, Histogram)
    """
    try:
        # Calculate EMAs
        ema_fast = df['close'].ewm(span=fast_period, adjust=False).mean()
        ema_slow = df['close'].ewm(span=slow_period, adjust=False).mean()
        
        # Calculate MACD line
        macd_line = ema_fast - ema_slow
        
        # Calculate signal line
        signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
        
        # Calculate histogram
        histogram = macd_line - signal_line
        
        # Create result DataFrame with explicit column names
        result = pd.DataFrame({
            'DIFF': macd_line,  # Fast EMA - Slow EMA
            'DEA': signal_line,  # Signal line (EMA of MACD)
            'BAR': histogram  # MACD histogram (MACD - Signal)
        })
        
        return result
    except Exception as e:
        logger.error(f"Error calculating MACD: {str(e)}", exc_info=True)
        raise

def plot_macd(df: pd.DataFrame, macd_df: pd.DataFrame, symbol: str, time_level: str, output_dir: str) -> None:
    """
    Plot MACD indicator and save to file.
    
    Args:
        df: Original stock data DataFrame
        macd_df: DataFrame with MACD values
        symbol: Stock symbol
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
        
        # Calculate crossover points
        # Golden cross (DIFF crosses above DEA)
        golden_cross = (macd_df['DIFF'] > macd_df['DEA']) & (macd_df['DIFF'].shift(1) <= macd_df['DEA'].shift(1))
        # Death cross (DIFF crosses below DEA)
        death_cross = (macd_df['DIFF'] < macd_df['DEA']) & (macd_df['DIFF'].shift(1) >= macd_df['DEA'].shift(1))
        
        # Plot MACD lines
        ax2.plot(macd_df.index, macd_df['DIFF'], label='DIFF', color='blue')
        ax2.plot(macd_df.index, macd_df['DEA'], label='DEA', color='red')
        
        # Plot histogram as bar chart
        # Color bars based on value: green for positive, red for negative
        positive_bars = macd_df['BAR'] >= 0
        negative_bars = macd_df['BAR'] < 0
        
        ax2.bar(macd_df.index[positive_bars], macd_df['BAR'][positive_bars], 
                label='BAR (Positive)', color='green', alpha=0.6)
        ax2.bar(macd_df.index[negative_bars], macd_df['BAR'][negative_bars], 
                label='BAR (Negative)', color='red', alpha=0.6)
        
        # Mark golden crosses
        golden_points = macd_df[golden_cross]
        if not golden_points.empty:
            ax2.scatter(golden_points.index, golden_points['DIFF'], 
                       marker='^', color='gold', s=100, label='Golden Cross', zorder=5)
        
        # Mark death crosses
        death_points = macd_df[death_cross]
        if not death_points.empty:
            ax2.scatter(death_points.index, death_points['DIFF'], 
                       marker='v', color='purple', s=100, label='Death Cross', zorder=5)
        
        ax2.set_title(f'{symbol} - MACD Indicator')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('MACD Value')
        ax2.legend()
        ax2.grid(True)
        
        # Save plot
        plot_filename = os.path.join(output_dir, f'{symbol}_{time_level}_macd.png')
        plt.tight_layout()
        plt.savefig(plot_filename)
        plt.close()
        
        logger.info(f"Saved MACD plot to {plot_filename}")
    except Exception as e:
        logger.error(f"Error plotting MACD: {str(e)}", exc_info=True)
        raise

def calculate_and_save_macd(symbol: str, time_level: str, data_dir: str = './output', output_dir: str = './output/macd') -> None:
    """
    Calculate MACD for given symbol and time level, save results to CSV and plot.
    
    Args:
        symbol: Stock symbol
        time_level: Time level (e.g., '1_minute', '5_minute', '1_day')
        data_dir: Directory containing stock data CSV files
        output_dir: Base output directory for MACD results
    """
    try:
        # Create symbol-specific output directory with time level
        symbol_output_dir = os.path.join(output_dir, symbol, 'indicators', 'macd', time_level)
        
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
        
        # Calculate MACD
        macd_df = calculate_macd(df)
        
        # Save MACD to CSV
        if not os.path.exists(symbol_output_dir):
            os.makedirs(symbol_output_dir)
            logger.info(f"Created symbol directory: {symbol_output_dir}")
        
        csv_filename = os.path.join(symbol_output_dir, f'{symbol}_{time_level}_macd.csv')
        
        # Check if CSV file already exists
        if os.path.exists(csv_filename):
            logger.info(f"MACD data already exists for {symbol} {time_level}, skipping calculation")
            return
        
        macd_df.to_csv(csv_filename)
        logger.info(f"Saved MACD data to {csv_filename}")
        
        # Plot MACD
        plot_macd(df, macd_df, symbol, time_level, symbol_output_dir)
        
    except Exception as e:
        logger.error(f"Error calculating and saving MACD for {symbol} {time_level}: {str(e)}", exc_info=True)
        raise