# Portfolio Analysis - Claude Context

## Project Overview

This is an AI-powered portfolio analysis tool that helps investors analyze their stock holdings and develop optimization strategies for reducing over-leveraged positions. The tool uses a multi-agent architecture built on the Agno framework with AWS Bedrock models.

## Architecture

### Core Components

1. **Configuration System** (`Config` class)
   - Environment-based configuration management
   - Validates all required environment variables on startup
   - Supports flexible model selection via AWS Bedrock model IDs

2. **Portfolio Agent**
   - **Purpose**: Analyzes CSV files containing portfolio holdings
   - **Tools**: CsvTools for reading and analyzing CSV data
   - **Model**: Configurable AWS Bedrock model
   - **Instructions**: Reads all CSV files to gather complete holding details

3. **Finance Agent**
   - **Purpose**: Provides real-time market data and financial analysis
   - **Tools**: YFinanceTools with specific capabilities:
     - Current stock prices
     - Company information
     - Historical price data
     - Analyst recommendations
     - Company news
   - **Model**: Configurable AWS Bedrock model
   - **Instructions**: Provides accurate financial information for the specified stock ticker

4. **Portfolio Analysis Team**
   - **Purpose**: Coordinates both agents to generate comprehensive analysis
   - **Members**: Portfolio Agent + Finance Agent
   - **Model**: Configurable AWS Bedrock model (team coordinator)
   - **Output**: Comprehensive position analysis with detailed optimization strategy

### Design Decisions

- **AWS Bedrock**: Chosen to allow model configuration without code changes
- **Multi-agent approach**: Separates portfolio data analysis from market data retrieval for better modularity
- **Team coordination**: Combines insights from both agents for holistic analysis
- **Environment-based config**: All settings externalized for easy deployment and testing

## Current Functionality

### What It Does
1. Loads portfolio data from multiple CSV files (supports multiple brokerage accounts)
2. Fetches current market data for specified stock ticker
3. Analyzes holdings against current market conditions
4. Generates a detailed sell-off strategy to avoid over-leverage
5. Provides specific recommendations with timing for selling positions

### Input Requirements
- CSV files with portfolio holdings (from brokerage accounts)
- Stock ticker symbol to analyze
- AWS Bedrock model IDs for each agent
- AWS credentials configured for Bedrock access

### Output
- Comprehensive position analysis
- Detailed optimization strategy
- Specific action plan with timing for selling positions
- Uses all individual stock details (not just summaries)

## File Structure

```
financeagent/
├── portfolio_analysis.py    # Main application file
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (not in repo)
├── .gitignore               # Git ignore rules
├── README.md                # User documentation
└── CLAUDE.md                # This file - Claude context
```

## Key Functions

### `validate_environment_variables()`
- **Location**: portfolio_analysis.py:23
- Validates presence of all required environment variables
- Exits with error message if any are missing

### `get_csv_files_os(folder_path)`
- **Location**: portfolio_analysis.py:43
- Scans folder for CSV files
- Returns list of absolute paths to all CSV files

### `create_agents(config)`
- **Location**: portfolio_analysis.py:50
- Instantiates portfolio agent, finance agent, and team
- Executes the analysis query
- Streams results to console

## Suggested Improvement Phases

### Phase 1: Core Enhancements
**Goal**: Improve robustness and user experience

- [ ] Add error handling for CSV parsing failures
- [ ] Implement logging framework (replace print statements)
- [ ] Add support for multiple stock tickers in a single run
- [ ] Create output file with analysis results (JSON/PDF)
- [ ] Add progress indicators for long-running analyses
- [ ] Validate CSV structure and provide helpful error messages
- [ ] Add dry-run mode to preview without executing

### Phase 2: Advanced Analysis Features
**Goal**: Expand analytical capabilities

- [ ] Support portfolio diversification analysis
- [ ] Add tax-loss harvesting recommendations
- [ ] Include portfolio rebalancing suggestions
- [ ] Add risk analysis metrics (Sharpe ratio, beta, etc.)
- [ ] Support sector allocation analysis
- [ ] Add comparison against benchmark indices (S&P 500, etc.)
- [ ] Include dividend income analysis
- [ ] Support what-if scenario modeling

### Phase 3: Data Integration
**Goal**: Expand data sources and formats

- [ ] Support additional data sources beyond YFinance
- [ ] Add support for cryptocurrency portfolios
- [ ] Integrate with brokerage APIs (Robinhood, TD Ameritrade, etc.)
- [ ] Support Excel files in addition to CSV
- [ ] Add real-time portfolio tracking
- [ ] Include economic indicators in analysis
- [ ] Support international markets and currencies

### Phase 4: User Interface
**Goal**: Make the tool more accessible

- [ ] Create CLI with argparse for better command-line experience
- [ ] Add interactive mode for configuration
- [ ] Build web UI for portfolio visualization
- [ ] Create dashboard with charts and graphs
- [ ] Add email/SMS notifications for recommendations
- [ ] Support scheduled analysis runs
- [ ] Add portfolio comparison features

### Phase 5: Architecture & Testing
**Goal**: Improve code quality and maintainability

- [ ] Refactor into modular package structure
- [ ] Add comprehensive unit tests
- [ ] Add integration tests with mocked data
- [ ] Implement CI/CD pipeline
- [ ] Add type hints throughout codebase
- [ ] Create Docker container for easy deployment
- [ ] Add configuration validation schema
- [ ] Implement caching for API calls to reduce costs
- [ ] Add retry logic for API failures

### Phase 6: Advanced AI Features
**Goal**: Leverage AI capabilities more deeply

- [ ] Add natural language query interface
- [ ] Support custom analysis questions
- [ ] Include sentiment analysis from news sources
- [ ] Add predictive modeling for price movements
- [ ] Create personalized investment recommendations
- [ ] Support risk tolerance profiling
- [ ] Add explainable AI features for transparency
- [ ] Include multi-language support

### Phase 7: Compliance & Security
**Goal**: Make production-ready for sensitive financial data

- [ ] Add data encryption at rest and in transit
- [ ] Implement audit logging for all operations
- [ ] Add user authentication and authorization
- [ ] Support PII data masking in logs
- [ ] Add compliance reporting (SEC, FINRA, etc.)
- [ ] Implement rate limiting for API calls
- [ ] Add data retention policies
- [ ] Create security documentation

## Known Limitations

1. **Single Stock Focus**: Currently analyzes one stock ticker at a time
2. **No Historical Tracking**: Doesn't maintain history of previous analyses
3. **Limited Error Handling**: Minimal error recovery for API failures
4. **Console Output Only**: No persistent output or reporting
5. **Manual CSV Management**: Requires manual download and placement of CSV files
6. **No Cost Optimization**: No caching or batching of API calls
7. **AWS Bedrock Only**: Locked into AWS Bedrock for AI models
8. **No Testing**: No automated tests for reliability

## Environment Variables Reference

```bash
# Required
PORTFOLIO_CSVS_LOCATION=/path/to/csv/files
FINANCE_AGENT_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
PORTFOLIO_AGENT_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
PORTFOLIO_ANALYSIS_TEAM_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
STOCK_TICKER=COF

# AWS Credentials (set via AWS CLI or environment)
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_REGION=us-east-1
```

## Dependencies

- **agno**: AI agent framework for building multi-agent systems
- **yfinance**: Yahoo Finance API wrapper for market data
- **python-dotenv**: Environment variable management
- **boto3**: AWS SDK for Bedrock access

## Common Tasks for Claude

### Adding a New Agent
1. Create new Agent instance in `create_agents()` function
2. Configure with appropriate tools and instructions
3. Add to Team members list
4. Update environment variables if new model needed

### Modifying Analysis Query
- Edit the query string in portfolio_analysis.py:90-92
- Query determines what analysis the team performs

### Adding New Data Sources
1. Import new tool (e.g., from agno.tools)
2. Add to appropriate agent's tools list
3. Update agent instructions to use new tool

### Changing Output Format
- Modify `print_response()` call in portfolio_analysis.py:90
- Add file writing logic after team execution
- Consider adding output format configuration

## Testing Checklist

When making changes, verify:
- [ ] All environment variables are validated
- [ ] CSV files are correctly discovered and loaded
- [ ] API calls to YFinance succeed
- [ ] AWS Bedrock models are accessible
- [ ] Team coordination produces coherent output
- [ ] Error messages are helpful and actionable
- [ ] Output is properly formatted in markdown

## Quick Start for Development

```bash
# Setup
pip install -r requirements.txt
cp .env.example .env  # Edit with your values

# Run
python portfolio_analysis.py

# Test with different models
# Edit .env and change model IDs, then re-run
```
