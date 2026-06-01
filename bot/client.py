from dotenv import load_dotenv
from pathlib import Path
import os
from binance.client import Client

# Load .env file
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Read API keys
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")



if not API_KEY or not API_SECRET:
    raise ValueError("API keys not found in .env file")

# Create Binance client
client = Client(API_KEY, API_SECRET)

# Binance Futures Testnet URL
client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"