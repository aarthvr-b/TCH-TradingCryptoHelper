import json
import os

TRADE_LOG = "trades.json"


def load_trades():
    """Load all trades from JSON file"""
    if not os.path.exists(TRADE_LOG):
        # Create empty file to prevent JSON errors
        with open(TRADE_LOG, "w") as f:
            json.dump([], f)
        return []

    try:
        with open(TRADE_LOG, "r") as f:
            content = f.read().strip()
            if not content:
                return []  # Empty file
            return json.loads(content)
    except (json.JSONDecodeError, OSError):
        return []


def save_trades(trades):
    """save all trades back to json file."""
    with open(TRADE_LOG, "w") as f:
        json.dump(trades, f, indent=4)
