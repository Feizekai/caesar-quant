import yaml
import logging
import os

logger = logging.getLogger(__name__)

def load_factors_config(config_path="config/factors.yaml"):
    """Load factors configuration from YAML file"""
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        logger.error(f"Error loading factors config: {str(e)}", exc_info=True)
        return None

def load_symbols_config(config_path="config/symbols.yaml"):
    """Load symbols configuration from YAML file"""
    try:
        # Check if the config file exists in the current directory
        if not os.path.exists(config_path):
            # If not, try to find it relative to the script location
            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(script_dir, 'symbols.yaml')
        
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        logger.error(f"Error loading symbols config: {str(e)}", exc_info=True)
        return None

def get_symbols(config):
    """Extract symbols from configuration"""
    if not config or 'symbols' not in config:
        logger.error("Symbols not found in config")
        return []
    
    return config['symbols']

def get_technical_indicators(config):
    """Extract technical indicators configuration"""
    if not config or 'technical' not in config:
        logger.error("Technical indicators not found in config")
        return None
    
    return config['technical']

def get_minute_levels(config):
    """Extract minute levels from technical indicators configuration"""
    technical = get_technical_indicators(config)
    if not technical:
        return []
    
    minute_levels = []
    for item in technical:
        if 'minute_level' in item:
            minute_levels.append(item['minute_level'])
    
    return minute_levels