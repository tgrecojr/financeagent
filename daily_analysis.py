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
        self.daily_analysis_model = os.getenv("DAILY_ANALYSIS_MODEL")
        self.stock_ticker = os.getenv("STOCK_TICKER")


def validate_environment_variables():
    """Validate that all required environment variables are set."""
    required_vars = [
        "DAILY_ANALYSIS_MODEL",
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

    daily_agent = Agent(
        name="Daily Stock Analysis Agent",
        model=AwsBedrock(id=config.daily_analysis_model),
        tools=[
            YFinanceTools(
                include_tools=[
                    "get_current_stock_price",
                    "get_historical_stock_prices",                ]
            )
        ],
        markdown=True,

    )

    daily_agent.print_response(
        f"""For the stock ticker {config.stock_ticker}, perform a fundamental analysis (e.g., momentum data) by looking back at the last 100 days 
        to calculate the RSI(14), and MACD(12,26,9) values to determine a Decision status: "Buy", "Hold", or "Sell" based on:
        - Buy Signal: RSI < 30 (oversold) AND MACD > Signal (bullish crossover)
        - Sell Signal: RSI > 70 (overbought) AND MACD < Signal (bearish crossover)
        - Hold Signal: All other conditions (default recommendation)
        - Write a short, plain-language insight about what's happening
        - Use familiar terms like "gaining steam," "cooling off," or "showing hesitation"
        - Avoid technical jargon like RSI or MACD unless context makes it helpful
        - Add a helpful tip or comment for each stock (e.g., "This pattern often signals hesitation" or "This dip might attract bargain hunters")

        Finish with a summary line using the timestamp like this:
        Summary as of October 8, 2025 – Most stocks were stable with one or two worth watching.""",
        stream=True
    )


if __name__ == '__main__':
    load_dotenv()
    validate_environment_variables()
    config = Config()
    create_agents(config)