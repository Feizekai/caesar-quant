#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Caesar Quantitative Analysis System
主入口文件
"""

import argparse
import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from command.cli import fetch_stock_data_command

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Caesar Quantitative Analysis System')
    parser.add_argument('--mode', choices=['train', 'backtest', 'serve', 'fetch', 'calculate'], 
                        default='train', help='运行模式')
    
    # Parse known args to get the mode first
    args, remaining = parser.parse_known_args()
    
    if args.mode == 'fetch':
        # Parse fetch-specific arguments
        fetch_parser = argparse.ArgumentParser()
        fetch_parser.add_argument('--symbol', required=False, help='Stock symbol to fetch data for (optional, fetches all symbols if not provided)')
        fetch_parser.add_argument('--api-key', required=True, help='Alpha Vantage API key')
        fetch_parser.add_argument('--output', default='./output', help='Output directory for CSV files')
        
        # Parse only the arguments after --mode fetch
        fetch_args, _ = fetch_parser.parse_known_args(remaining)
        
        # Validate required arguments
        if not fetch_args.api_key:
            print("Error: --api-key is required for fetch mode")
            sys.exit(1)
        
        # Call the appropriate fetch function based on whether symbol is provided
        if fetch_args.symbol:
            from data.fetcher import fetch_stock_data
            fetch_stock_data(fetch_args.symbol, fetch_args.api_key, fetch_args.output)
        else:
            from data.fetcher import fetch_all_stocks_data
            fetch_all_stocks_data(fetch_args.api_key, fetch_args.output)
    elif args.mode == 'calculate':
        # Parse calculate-specific arguments
        calculate_parser = argparse.ArgumentParser()
        calculate_parser.add_argument('--indicator', required=True, choices=['macd', 'boll', 'rsi'], help='Indicator to calculate')
        calculate_parser.add_argument('--symbol', required=False, help='Stock symbol to calculate indicator for (optional, calculates for all symbols if not provided)')
        calculate_parser.add_argument('--time-level', required=False, help='Time level to calculate indicator for (optional, calculates for all time levels if not provided)')
        calculate_parser.add_argument('--data-dir', default='./output', help='Directory containing stock data CSV files')
        calculate_parser.add_argument('--output-dir', default='./output', help='Base output directory for results')
        
        # Parse only the arguments after --mode calculate
        calculate_args, _ = calculate_parser.parse_known_args(remaining)
        
        # Import and call the appropriate calculation function
        if calculate_args.indicator == 'macd':
            from indicators.macd import calculate_and_save_macd
            from config.reader import load_symbols_config, get_symbols
            
            # Get symbols to calculate for
            if calculate_args.symbol:
                symbols = [calculate_args.symbol]
            else:
                # Load symbols from config
                symbols_config = load_symbols_config()
                if symbols_config:
                    symbols = get_symbols(symbols_config)
                else:
                    symbols = []
            
            # Get time levels to calculate for
            if calculate_args.time_level:
                time_levels = [calculate_args.time_level]
            else:
                # Load time levels from config
                from config.reader import load_factors_config, get_minute_levels
                factors_config = load_factors_config()
                if factors_config:
                    time_levels = get_minute_levels(factors_config)
                    # Add day level if it exists in config
                    if '1_day' not in time_levels:
                        time_levels.append('1_day')
                else:
                    time_levels = []
            
            # Calculate MACD for each symbol and time level
            for symbol in symbols:
                for time_level in time_levels:
                    try:
                        calculate_and_save_macd(symbol, time_level, calculate_args.data_dir, calculate_args.output_dir)
                    except Exception as e:
                        print(f"Error calculating MACD for {symbol} {time_level}: {str(e)}")
        elif calculate_args.indicator == 'boll':
            from indicators.boll import calculate_and_save_boll
            from config.reader import load_symbols_config, get_symbols
            
            # Get symbols to calculate for
            if calculate_args.symbol:
                symbols = [calculate_args.symbol]
            else:
                # Load symbols from config
                symbols_config = load_symbols_config()
                if symbols_config:
                    symbols = get_symbols(symbols_config)
                else:
                    symbols = []
            
            # Get time levels to calculate for
            if calculate_args.time_level:
                time_levels = [calculate_args.time_level]
            else:
                # Load time levels from config
                from config.reader import load_factors_config, get_minute_levels
                factors_config = load_factors_config()
                if factors_config:
                    time_levels = get_minute_levels(factors_config)
                    # Add day level if it exists in config
                    if '1_day' not in time_levels:
                        time_levels.append('1_day')
                else:
                    time_levels = []
            
            # Calculate BOLL for each symbol and time level
            for symbol in symbols:
                for time_level in time_levels:
                    try:
                        calculate_and_save_boll(symbol, time_level, calculate_args.data_dir, calculate_args.output_dir)
                    except Exception as e:
                        print(f"Error calculating BOLL for {symbol} {time_level}: {str(e)}")
        elif calculate_args.indicator == 'rsi':
            from indicators.rsi import calculate_and_save_rsi
            from config.reader import load_symbols_config, get_symbols
            
            # Get symbols to calculate for
            if calculate_args.symbol:
                symbols = [calculate_args.symbol]
            else:
                # Load symbols from config
                symbols_config = load_symbols_config()
                if symbols_config:
                    symbols = get_symbols(symbols_config)
                else:
                    symbols = []
            
            # Get time levels to calculate for
            if calculate_args.time_level:
                time_levels = [calculate_args.time_level]
            else:
                # Load time levels from config
                from config.reader import load_factors_config, get_minute_levels
                factors_config = load_factors_config()
                if factors_config:
                    time_levels = get_minute_levels(factors_config)
                    # Add day level if it exists in config
                    if '1_day' not in time_levels:
                        time_levels.append('1_day')
                else:
                    time_levels = []
            
            # Calculate RSI for each symbol and time level
            for symbol in symbols:
                for time_level in time_levels:
                    try:
                        calculate_and_save_rsi(symbol, time_level, calculate_args.data_dir, calculate_args.output_dir)
                    except Exception as e:
                        print(f"Error calculating RSI for {symbol} {time_level}: {str(e)}")
    else:
        # Handle other modes (train, backtest, serve)
        # For now, we'll just print a message as CLI class is not defined
        print(f"Mode '{args.mode}' is not yet implemented")


if __name__ == '__main__':
    main()