# Caesar Quantitative Analysis System

这是一个Python量化分析系统，我将其命名为凯撒，源于我对于古罗马个人英雄主义的敬仰。希望我们每个人都能成为自己和家人的英雄。
『这是一个有想法就能挣到钱的时代』 from Robin

## 项目结构

```ini
caesar-quant/
├── config/              # 配置读取模块
│   ├── __init__.py
│   ├── config.yaml      # 配置文件（股票列表，因子策略列表，回测结果列表）
│   └── reader.py        # 配置读取器
├── data/                # 数据抓取模块
│   ├── __init__.py
│   ├── fetcher.py       # 数据抓取器（抓取目标股票的数据）
│   └── feature_engineer.py  # 特征工程化处理
├── factors/             # 因子处理根目录
│   ├── __init__.py
│   ├── extract/         # 因子提取模块
│   │   ├── __init__.py
│   │   └── extractor.py # 因子提取器
│   ├── train/           # 因子训练模块
│   │   ├── __init__.py
│   │   └── trainer.py   # 因子训练器
│   └── backtest/        # 因子回测模块
│       ├── __init__.py
│       └── backtester.py # 回测器
├── cache/               # 缓存模块
│   ├── __init__.py
│   └── manager.py       # 缓存管理器
├── mcp/                 # MCP模块
│   ├── __init__.py
│   └── server.py        # MCP服务接口
├── api/                 # API模块
│   ├── __init__.py
│   └── server.py        # HTTP服务接口
├── command/             # 命令行模块
│   ├── __init__.py
│   └── cli.py           # 命令行接口
├── main.py              # 主入口文件
└── requirements.txt     # 项目依赖
```

## 模块功能说明

### 配置读取模块 (config)

- 读取配置文件中的股票列表、因子策略列表、回测结果列表

### 数据抓取模块 (data)

- 抓取目标股票的数据
- 对数据进行特征工程化处理
- 调用大模型搜集舆情

### 因子处理模块 (factors)

#### 因子提取 (factors/extract)

- 读取因子配置
- 从特征化后的数据中抓取因子

#### 因子训练 (factors/train)

- 对提取的因子进行训练

#### 因子回测 (factors/backtest)

- 对因子进行不同分钟级别的回测
- 记录每只股票在当前最好的策略
- 将结果写入持久化存储

### 缓存模块 (cache)

- 负责缓存的构建和写入

### MCP模块 (mcp)

- 提供MCP接口给到大模型

### API模块 (api)

- 对外提供HTTP接口

### 命令行模块 (command)

- 封装命令行及启动类