#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Caesar Quantitative Analysis System
主入口文件
"""

import argparse
from command.cli import CLI


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Caesar Quantitative Analysis System')
    parser.add_argument('--mode', choices=['train', 'backtest', 'serve'], 
                        default='train', help='运行模式')
    args = parser.parse_args()
    
    cli = CLI()
    
    if args.mode == 'train':
        cli.train()
    elif args.mode == 'backtest':
        cli.backtest()
    elif args.mode == 'serve':
        cli.serve()


if __name__ == '__main__':
    main()