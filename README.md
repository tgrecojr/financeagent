# Portfolio Analysis

A financial portfolio analysis tool that uses AI agents to analyze stock portfolios and provide optimization strategies for selling off holdings to avoid over-leverage, plus daily technical analysis for individual stocks.

## Overview

This tool uses AWS Bedrock-powered AI agents to:
- Analyze portfolio holdings from CSV files
- Gather real-time financial data and market analysis for specific stocks
- Generate comprehensive position analysis and detailed optimization strategies
- Provide actionable sell-off plans over time
- Perform daily technical analysis with RSI, MACD, and plain-language insights

**Why AWS Bedrock?** This implementation uses AWS Bedrock to allow you to configure and switch between different AI models without changing code. Simply update the model IDs in your `.env` file to experiment with different models and find the best performance for your analysis needs.

## Features

### Portfolio Analysis (portfolio_analysis.py)
- **Portfolio Agent**: Reads and analyzes CSV files containing your stock holdings
- **Finance Agent**: Retrieves current stock prices, company info, historical data, analyst recommendations, and company news using YFinance
- **Team Collaboration**: Combines both agents to provide comprehensive analysis and optimization strategies

### Daily Technical Analysis (daily_analysis.py)
- **Daily Analysis Agent**: Performs technical analysis on individual stocks
- **RSI & MACD Calculations**: Analyzes 100 days of historical data to calculate RSI(14) and MACD(12,26,9)
- **Buy/Hold/Sell Signals**: Generates actionable recommendations based on technical indicators
- **Plain-Language Insights**: Provides easy-to-understand market commentary without jargon

## Requirements

- Python 3.x
- AWS Bedrock access
- Required Python packages (see requirements.txt)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with the following required variables:

**For Portfolio Analysis:**
```
PORTFOLIO_CSVS_LOCATION=/path/to/your/csv/files
FINANCE_AGENT_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
PORTFOLIO_AGENT_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
PORTFOLIO_ANALYSIS_TEAM_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
STOCK_TICKER=NFLX
```

**For Daily Analysis:**
```
DAILY_ANALYSIS_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
STOCK_TICKER=NFLX
```

**AWS Bedrock Model ID Examples:**
- `global.anthropic.claude-sonnet-4-20250514-v1:0` - Claude 4 Sonnet 
- `anthropic.claude-3-5-sonnet-20241022-v2:0` - Claude 3.5 Sonnet
- `anthropic.claude-3-5-haiku-20241022-v1:0` - Claude 3.5 Haiku (faster, lower cost)
- `anthropic.claude-3-opus-20240229-v1:0` - Claude 3 Opus (most capable)
- `amazon.nova-pro-v1:0` - Amazon Nova Pro
- `amazon.nova-lite-v1:0` - Amazon Nova Lite

You can mix and match different models for each agent based on your performance and cost requirements.

3. Prepare your portfolio data:
   - Go to each of your brokerage accounts
   - Download your full portfolio in CSV format
   - Place all CSV files in the location specified by `PORTFOLIO_CSVS_LOCATION`

## Usage

### Portfolio Analysis

Run the portfolio analysis:

```bash
python portfolio_analysis.py
```

The tool will:
1. Validate all required environment variables
2. Load portfolio data from CSV files
3. Fetch current market data for the specified stock ticker
4. Generate a comprehensive position analysis
5. Provide a detailed optimization strategy with specific sell-off recommendations

### Daily Technical Analysis

Run the daily analysis:

```bash
python daily_analysis.py
```

The tool will:
1. Validate required environment variables
2. Fetch 100 days of historical price data for the specified stock ticker
3. Calculate RSI(14) and MACD(12,26,9) technical indicators
4. Generate a Buy/Hold/Sell recommendation based on:
   - **Buy Signal**: RSI < 30 (oversold) AND MACD > Signal (bullish crossover)
   - **Sell Signal**: RSI > 70 (overbought) AND MACD < Signal (bearish crossover)
   - **Hold Signal**: All other conditions
5. Provide plain-language insights and helpful tips

## Configuration

All configuration is managed through environment variables:

### Portfolio Analysis Variables
- `PORTFOLIO_CSVS_LOCATION`: Path to folder containing portfolio CSV files
- `FINANCE_AGENT_MODEL`: AWS Bedrock model ID for the finance agent
- `PORTFOLIO_AGENT_MODEL`: AWS Bedrock model ID for the portfolio agent
- `PORTFOLIO_ANALYSIS_TEAM_MODEL`: AWS Bedrock model ID for the team coordinator
- `STOCK_TICKER`: Stock ticker symbol to analyze (e.g., NFLX for Netflix)

### Daily Analysis Variables
- `DAILY_ANALYSIS_MODEL`: AWS Bedrock model ID for the daily analysis agent
- `STOCK_TICKER`: Stock ticker symbol to analyze (e.g., NFLX for Netflix)

## Dependencies

- `agno`: AI agent framework
- `yfinance`: Yahoo Finance data retrieval
- `python-dotenv`: Environment variable management
- `boto3`: AWS SDK for Python (Bedrock access)
