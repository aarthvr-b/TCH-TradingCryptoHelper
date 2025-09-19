### calculator.py
### This file handles position size, leverage and fee calculations

def calculate_position(account_size, risk_pct, entry, stop_loss):
    """
    Calculate trade position size, leverage, and fees.

    Args:
        account_size (float): Total USDT in account
        risk_pct (float): Risk per trade in percent (1-3%)
        entry (float): Entry price
        stop_loss (float): Stop loss price

    Returns: 
        dict: {
        "risk_usdt" : float,
        "position_size" : float,
        "order_value" : float,
        "required_leverage": float,
        "leverage_note": str,
        "taker_fee": float,
        "maker_fee" float:
        }
    """

    # Risk in USDT
    risk_amount = account_size * (risk_pct / 100)

    # Distance between entry and stop loss
    stop_distance = abs(entry - stop_loss)
    if stop_distance == 0:
        raise ValueError("Stop loss cannot be equal to entry price.")

    # Position size
    position_size = risk_amount / stop_distance
    order_value = position_size * entry

    # Check Leverage
    if order_value <= account_size:
        leverage = 1.0
        leverage_note = "No leverage required"
    else:
        leverage = order_value / account_size
        leverage_note = f"Leverage required: {leverage:.2f}x"

    # Fees
    taker_fee = order_value * 0.00055
    maker_fee = order_value * 0.0002

    return {
        "risk_amount" : risk_amount,
        "position_size" : position_size,
        "order_value" : order_value,
        "required_leverage": leverage,
        "leverage_note": leverage_note,
        "taker_fee":taker_fee,
        "maker_fee": maker_fee
    }
