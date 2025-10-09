### calculator.py
### This file handles quantity size, leverage and fee calculations


def calculate_quantity(account_size, risk_pct, entry, stop_loss):
    """
    Calculate trade quantity size, leverage, and fees.

    Args:
        account_size (float): Total USDT in account
        risk_pct (float): Risk per trade in percent (1-3%)
        entry (float): Entry price
        stop_loss (float): Stop loss price

    Returns:
        dict: {
        "risk_usdt" : float,
        "quantity" : float,
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

    # quantity size
    quantity = risk_amount / stop_distance
    order_value = quantity * entry

    # Required leverage
    required_leverage = order_value / account_size
    if required_leverage < 1:
        required_leverage = 1.0
    required_leverage = round(required_leverage, 1)

    if required_leverage == 1.0:
        leverage_note = "✅ No leverage required"
    elif required_leverage <= 10:
        leverage_note = f"⚠️ Order value ({order_value:.2f} USDT) exceeds account size! Moderate leverage suggested: {required_leverage:.1f}×"
    else:
        leverage_note = f"🚨 Order value ({order_value:.2f} USDT) exceeds account size! High leverage required: {required_leverage:.1f}×"

    # Fees
    taker_fee = order_value * 0.00055
    maker_fee = order_value * 0.0002

    return {
        "risk_amount": risk_amount,
        "quantity": quantity,
        "order_value": order_value,
        "required_leverage": required_leverage,
        "leverage_note": leverage_note,
        "taker_fee": taker_fee,
        "maker_fee": maker_fee,
    }
