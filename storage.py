import json 
import os

TRADE_LOG = "trades.json"

def load_trades():
    """Load all trades from JSON file"""
    if not os.path.exists(TRADE_LOG):
        return []
    with open(TRADE_LOG, "r") as f:
        return json.load(f)

def save_trades(trades):
    """save all trades back to json file."""
    with open(TRADE_LOG, "w") as f:
        json.dump(trades, f, indent=4)
