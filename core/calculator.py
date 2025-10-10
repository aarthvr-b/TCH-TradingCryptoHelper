### calculator.py
### This file handles quantity size, leverage and fee calculations


def calculate_quantity(
    account_size, risk_pct, entry, stop_loss, mmr=0.005, direction="long"
):
    """
    Calculate trade quantity size, leverage, and fees.

    Args:
        account_size (float): Total USDT in account
        risk_pct (float): Risk per trade in percent (1-3%)
        entry (float): Entry price
        stop_loss (float): Stop loss price
        mmr (float): Maintenance margin rate (default 0.005 for 0.5%)

    Returns:
        dict: {
        "risk_usdt" : float,
        "quantity" : float,
        "order_value" : float,
        "required_leverage": float,
        "leverage_note": str,
        "liquidation_price": float,
        "liquidation_warning": str,
        "taker_fee": float,
        "maker_fee" float:
        }
    """

    # --- Basic Risk and sizing ---
    risk_amount = account_size * (risk_pct / 100)
    stop_distance = abs(entry - stop_loss)
    if stop_distance == 0:
        raise ValueError("Stop loss cannot be equal to entry price.")

    quantity = round(risk_amount / stop_distance)
    order_value = quantity * entry

    # Required leverage
    required_leverage = max(1.0, round(order_value / account_size, 1))
    if required_leverage == 1.0:
        leverage_note = "✅ No leverage required"
    elif required_leverage <= 10:
        leverage_note = f"⚠️ Order value ({order_value:.2f} USDT) exceeds account size! Moderate leverage suggested: {required_leverage:.1f}×"
    else:
        leverage_note = f"🚨 Order value ({order_value:.2f} USDT) exceeds account size! High leverage required: {required_leverage:.1f}×"

    # --- Liquidation price calculation (Isolated Margin Model) ---
    if direction.lower() == "long":
        liquidation_price = entry * (
            1 - (1 / required_leverage) + (mmr / required_leverage)
        )
        stop_before_liq = stop_loss > liquidation_price
    else:
        liquidation_price = entry * (
            1 + (1 / required_leverage) - (mmr / required_leverage)
        )
        stop_before_liq = stop_loss < liquidation_price

    # --- Liquidation safety checks ---
    liquidation_distance_pct = abs(liquidation_price - stop_loss) / entry * 100
    stop_drawdown_pct = abs(stop_loss - entry) / entry * 100

    if not stop_before_liq:
        liquidation_warning = "🚨 Stop loss is beyond liquidation price! Adjust stop loss. Or reduce leverage!"
        warning_level = "danger"
    elif liquidation_distance_pct < 2:
        liquidation_warning = f"🚨 Liqquidation only {liquidation_distance_pct:.2f}% away. - High risk trade"
        warning_level = "danger"
    elif liquidation_distance_pct < 6:
        liquidation_warning = (
            f"🟠 Liquidation {liquidation_distance_pct:.2f}% away - tight margin."
        )
        warning_level = "risky"
    elif liquidation_distance_pct < 15:
        liquidation_warning = (
            f"🟡 Liquidation {liquidation_distance_pct:.2f}% away - reasonable margin."
        )
        warning_level = "watch"
    else:
        liquidation_warning = (
            "✅ Stop loss is at a safe distance from liquidation price."
        )
        warning_level = "safe"

    liquidation_extra_info = (
        f"Stop drawdown: {stop_drawdown_pct:.2f}% | "
        f"Liquidation distance: {liquidation_distance_pct:.2f}%"
    )

    # Fees
    taker_fee = order_value * 0.00055
    maker_fee = order_value * 0.0002

    return {
        "risk_amount": risk_amount,
        "quantity": quantity,
        "order_value": order_value,
        "required_leverage": required_leverage,
        "leverage_note": leverage_note,
        "liquidation_price": liquidation_price,
        "liquidation_warning": liquidation_warning,
        "warning_level": warning_level,
        "taker_fee": taker_fee,
        "maker_fee": maker_fee,
    }
