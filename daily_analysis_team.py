from agno.agent import Agent
from agno.models.openai import OpenAIChat
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
        self.daily_analysis_model = os.getenv("DAILY_ANALYSIS_MODEL")
        self.stock_ticker = os.getenv("STOCK_TICKER")
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")


def validate_environment_variables():
    """Validate that all required environment variables are set."""
    required_vars = [
        "DAILY_ANALYSIS_MODEL",
        "STOCK_TICKER",
        "OPENROUTER_API_KEY"
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

    history_agent = Agent(
        name="Historical Stock Retreival AI Agent",
        model=OpenAIChat(
            id=config.daily_analysis_model,
            api_key=config.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1"
        ),
        tools=[
            YFinanceTools(
                include_tools=[
                    "get_current_stock_price",
                    "get_historical_stock_prices",
                ]
            )
        ],
        instructions=[f"Use the tool provided to return the last 100 days of market open,close, high, low, and volume data for {config.stock_ticker} stock"],
        markdown=True,
    )

    tech_analysis_agent = Agent(
        name="Technical Analysis AI Agent",
        model=OpenAIChat(
            id=config.daily_analysis_model,
            api_key=config.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1"
        ),
        instructions=[f"""Looking back at the last 100 days to calculate the RSI(14), and MACD(12,26,9) values to determine a Decision status: "Buy", "Hold", or "Sell" based on:
        - Buy Signal: RSI < 30 (oversold) AND MACD > Signal (bullish crossover)
        - Sell Signal: RSI > 70 (overbought) AND MACD < Signal (bearish crossover)
        - Hold Signal: All other conditions (default recommendation)"""],
        markdown=True,
    )

    summary_analysis_team = Team(
        name="Daily Stock Analysis Team",
        model=OpenAIChat(
            id=config.daily_analysis_model,
            api_key=config.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1"
        ),
        members=[history_agent, tech_analysis_agent],
        markdown=True,
    )


    summary_analysis_team.print_response(
        f"""For the stock ticker {config.stock_ticker}:
        - Write a short, plain-language insight about what's happening
        - Use familiar terms like "gaining steam," "cooling off," or "showing hesitation"
        - Avoid technical jargon like RSI or MACD unless context makes it helpful
        - Add a helpful tip or comment for each stock (e.g., "This pattern often signals hesitation" or "This dip might attract bargain hunters")

        Finish with a summary line using the timestamp like this:
        Summary as of October 8, 2025 – Most stocks were stable with one or two worth watching.""",
        stream=True
    )

    summary_agent = Agent(
        name="Summary Stock Analysis Analysis Agent",
        model=OpenAIChat(
            id=config.daily_analysis_model,
            api_key=config.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1"
        ),
        markdown=True,

    )


if __name__ == '__main__':
    load_dotenv()
    validate_environment_variables()
    config = Config()
    create_agents(config)