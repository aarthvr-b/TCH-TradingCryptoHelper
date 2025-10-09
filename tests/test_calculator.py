# tests/test_calculator.py
import pytest

from core.calculator import calculate_quantity


def test_stop_loss_equal_entry():
    """Stop loss equal to entry should raise ValueError"""
    account_size = 1000
    risk_pct = 2
    entry = 25000
    stop_loss = 25000  # Same as entry

    with pytest.raises(ValueError):
        calculate_quantity(account_size, risk_pct, entry, stop_loss)


def test_short_trade_quantity():
    """Short trade (entry > stop loss) should calculate positive quantity size"""
    account_size = 1000
    risk_pct = 2
    entry = 25000
    stop_loss = 24500  # Entry > stop loss, short trade

    result = calculate_quantity(account_size, risk_pct, entry, stop_loss)

    stop_distance = abs(entry - stop_loss)
    expected_quantity = (account_size * (risk_pct / 100)) / stop_distance

    assert result["quantity"] == expected_quantity
    assert result["required_leverage"] > 0
    assert "leverage_note" in result


def test_calculate_quantity_long():
    # Example inputs
    account_size = 1000
    risk_pct = 2
    entry = 25000
    stop_loss = 24500

    result = calculate_quantity(account_size, risk_pct, entry, stop_loss)

    # Check keys exists

    assert "quantity" in result
    assert "order_value" in result
    assert "required_leverage" in result
    assert "risk_amount" in result

    # Check calculations
    expected_risk = account_size * (risk_pct / 100)
    assert result["risk_amount"] == expected_risk

    stop_distance = abs(entry - stop_loss)
    expected_quantity = expected_risk / stop_distance
    assert result["quantity"] == expected_quantity

    # Leverage should be correct
    expected_order_value = expected_quantity * entry
    expected_leverage = expected_order_value / account_size
    assert result["required_leverage"] == expected_leverage
