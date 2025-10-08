from ast import Load
from agno.agent import Agent
from agno.models.aws import AwsBedrock
from agno.tools.yfinance import YFinanceTools
from agno.tools.csv_toolkit import CsvTools
from agno.team import Team
from dotenv import load_dotenv
import os
import sys


os.environ['AGNO_TELEMETRY'] = 'False'

class Config:
    """Configuration object for portfolio analysis."""
    def __init__(self):
        self.portfolio_csv_location = os.getenv("PORTFOLIO_CSVS_LOCATION")
        self.finance_agent_model = os.getenv("FINANCE_AGENT_MODEL")
        self.portfolio_agent_model = os.getenv("PORTFOLIO_AGENT_MODEL")
        self.portfolio_analysis_team_model = os.getenv("PORTFOLIO_ANALYSIS_TEAM_MODEL")
        self.stock_ticker = os.getenv("STOCK_TICKER")


def validate_environment_variables():
    """Validate that all required environment variables are set."""
    required_vars = [
        "PORTFOLIO_CSVS_LOCATION",
        "FINANCE_AGENT_MODEL",
        "PORTFOLIO_AGENT_MODEL",
        "PORTFOLIO_ANALYSIS_TEAM_MODEL",
        "STOCK_TICKER"
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print("Error: The following required environment variables are not set:", file=sys.stderr)
        for var in missing_vars:
            print(f"  - {var}", file=sys.stderr)
        sys.exit(1)

def get_csv_files_os(folder_path):
    csv_files = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            csv_files.append(os.path.join(folder_path, filename))
    return csv_files

def create_agents(config):

    portfolio_agent = Agent(
        model=AwsBedrock(id=config.portfolio_agent_model),
        tools=[CsvTools(csvs=get_csv_files_os(config.portfolio_csv_location))],
        markdown=True,
        instructions=[
            "Read through all of these these CSV files to gather all of the details for all of my holdings"
        ],
    )

    # Initialize the agent
    finance_agent = Agent(
        name="Finance AI Agent",
        model=AwsBedrock(id=config.finance_agent_model),
        tools=[
            YFinanceTools(
                include_tools=[
                    "get_current_stock_price",
                    "get_company_info",
                    "get_historical_stock_prices",
                    "get_analyst_recommendations",
                    "get_company_news"
                ]
            )
        ],
        instructions=[f"Use the tools to provide accurate and concise financial information, stock price, market fundamentals, and historical analysis of the {config.stock_ticker} stock"],
        markdown=True,

    )

    portfolio_analysis_team = Team(
        name="Capital One Selloff Team",
        model=AwsBedrock(id=config.portfolio_analysis_team_model),
        members=[portfolio_agent, finance_agent],
        markdown=True,
        #instructions=["please give me a COMPREHENSIVE COF POSITION ANALYSIS & detailed OPTIMIZATION STRATEGY using all of my stock details (not summary) for selling off my COF portfolio to avoid being overleveraged.  I am looking for a specific plan of action over a course of time specifying which stocks to sell off at what times."],
    )


    portfolio_analysis_team.print_response(
        f"please give me a COMPREHENSIVE {config.stock_ticker} POSITION ANALYSIS & detailed OPTIMIZATION STRATEGY using all of my stock details (not summary) for selling off my {config.stock_ticker} portfolio to avoid being overleveraged.  I am looking for a specific plan of action over a course of time specifying which stocks to sell off at what times.", stream=True
    )


if __name__ == '__main__':
    load_dotenv()
    validate_environment_variables()
    config = Config()
    create_agents(config)