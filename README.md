# Portfolio Analysis

A financial portfolio analysis tool that uses AI agents to analyze stock portfolios and provide optimization strategies for selling off holdings to avoid over-leverage, plus daily technical analysis for individual stocks.

## Overview

This tool uses OpenRouter-powered AI agents to:
- Analyze portfolio holdings from CSV files
- Gather real-time financial data and market analysis for specific stocks
- Generate comprehensive position analysis and detailed optimization strategies
- Provide actionable sell-off plans over time
- Perform daily technical analysis with RSI, MACD, and plain-language insights

**Why OpenRouter?** This implementation uses OpenRouter to give you access to multiple AI providers (Anthropic, OpenAI, Google, Meta, and more) through a single API. You can configure and switch between different AI models without changing code. Simply update the model IDs in your `.env` file to experiment with different models and find the best performance for your analysis needs.

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
- OpenRouter API key (get one at https://openrouter.ai/)
- Required Python packages (see requirements.txt)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with the following required variables:

```bash
# OpenRouter API Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Portfolio Configuration
PORTFOLIO_CSVS_LOCATION=/path/to/your/csv/files
STOCK_TICKER=NFLX

# Model Configuration (OpenRouter model IDs)
FINANCE_AGENT_MODEL=anthropic/claude-sonnet-4.5
PORTFOLIO_AGENT_MODEL=anthropic/claude-sonnet-4.5
PORTFOLIO_ANALYSIS_TEAM_MODEL=anthropic/claude-sonnet-4.5
DAILY_ANALYSIS_MODEL=anthropic/claude-sonnet-4.5
```

**OpenRouter Model ID Examples:**
- `anthropic/claude-sonnet-4.5` - Claude 4.5 Sonnet (latest, most capable)
- `anthropic/claude-opus-4.5` - Claude 4.5 Opus (most intelligent)
- `anthropic/claude-3.5-sonnet` - Claude 3.5 Sonnet
- `openai/gpt-4` - OpenAI GPT-4
- `openai/gpt-4-turbo` - OpenAI GPT-4 Turbo
- `google/gemini-pro-1.5` - Google Gemini Pro 1.5
- `meta-llama/llama-3.1-70b-instruct` - Meta Llama 3.1 70B

For the full list of available models, visit: https://openrouter.ai/models

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

### Required Variables
- `OPENROUTER_API_KEY`: Your OpenRouter API key (get one at https://openrouter.ai/)
- `PORTFOLIO_CSVS_LOCATION`: Path to folder containing portfolio CSV files
- `STOCK_TICKER`: Stock ticker symbol to analyze (e.g., NFLX for Netflix)

### Portfolio Analysis Model Variables
- `FINANCE_AGENT_MODEL`: OpenRouter model ID for the finance agent
- `PORTFOLIO_AGENT_MODEL`: OpenRouter model ID for the portfolio agent
- `PORTFOLIO_ANALYSIS_TEAM_MODEL`: OpenRouter model ID for the team coordinator

### Daily Analysis Model Variables
- `DAILY_ANALYSIS_MODEL`: OpenRouter model ID for the daily analysis agent

## Dependencies

- `agno`: AI agent framework
- `yfinance`: Yahoo Finance data retrieval
- `python-dotenv`: Environment variable management
- `openai`: OpenAI SDK for Python (used to connect to OpenRouter API)
- `duckdb`: Database library used by CSV tools
