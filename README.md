# Caesar Quantitative Analysis System

This is a Python quantitative analysis system, which I named Caesar because of my admiration for the individual heroism of ancient Rome. I hope each of us can become a hero for ourselves and our families.
This is an era where having ideas can earn money. "- Robin

## Project Structure

```ini
caesar-quant/
├── config/              # Configuration module
│   ├── __init__.py
│   ├── config.yaml      # Configuration file (stock list, factor strategy list, backtest result list)
│   └── reader.py        # Configuration reader
├── data/                # Data fetching module
│   ├── __init__.py
│   ├── fetcher.py       # Data fetcher (fetching target stock data)
│   └── feature_engineer.py  # Feature engineering processing
├── factors/             # Factor processing root directory
│   ├── __init__.py
│   ├── extract/         # Factor extraction module
│   │   ├── __init__.py
│   │   └── extractor.py # Factor extractor
│   ├── train/           # Factor training module
│   │   ├── __init__.py
│   │   └── trainer.py   # Factor trainer
│   └── backtest/        # Factor backtesting module
│       ├── __init__.py
│       └── backtester.py # Backtester
├── cache/               # Cache module
│   ├── __init__.py
│   └── manager.py       # Cache manager
├── mcp/                 # MCP module
│   ├── __init__.py
│   └── server.py        # MCP service interface
├── api/                 # API module
│   ├── __init__.py
│   └── server.py        # HTTP service interface
├── command/             # Command line module
│   ├── __init__.py
│   └── cli.py           # Command line interface
├── main.py              # Main entry file
└── requirements.txt     # Project dependencies
```

## Module Function Descriptions

### Configuration Module (config)

- Read stock list, factor strategy list, and backtest result list from configuration files

### Data Fetching Module (data)

- Fetch data for target stocks
- Perform feature engineering on the data
- Call large models to collect public sentiment

### Factor Processing Module (factors)

#### Factor Extraction (factors/extract)

- Read factor configurations
- Extract factors from feature-engineered data

#### Factor Training (factors/train)

- Train extracted factors

#### Factor Backtesting (factors/backtest)

- Backtest factors at different minute levels
- Record the best strategy for each stock
- Write results to persistent storage

### Cache Module (cache)

- Responsible for cache construction and writing

### MCP Module (mcp)

- Provide MCP interface to large models

### API Module (api)

- Provide HTTP interface externally

### Command Line Module (command)

- Encapsulate command line and startup classes