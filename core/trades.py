from datetime import datetime

from rich import box
from rich.console import Console
from rich.table import Table
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Button

from core.calculator import calculate_quantity
from screens.popup_message import PopupMessage
from storage import load_trades, save_trades

console = Console()
FEE_RATES = {"maker": 0.0002, "taker": 0.00055}


def open_trade(
    pair: str,
    direction: str,
    account_size: float,
    risk_pct: float,
    entry: float,
    stop_loss: float,
):
    """Create and save a new trade with calculated position sizing."""
    results = calculate_quantity(account_size, risk_pct, entry, stop_loss)

    trades = load_trades()
    trade = {
        "id": len(trades) + 1,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pair": pair,
        "account_size": account_size,
        "risk_pct": risk_pct,
        "entry": entry,
        "stop_loss": stop_loss,
        "direction": direction,
        **results,
        "status": "open",
        "exit_price": None,
        "gross_pnl": None,
        "fees_paid": None,
        "net_pnl": None,
        "notes": None,
    }
    trades.append(trade)
    save_trades(trades)
    return trade


def get_open_trades():
    trades = load_trades()
    return [t for t in trades if t["status"] == "open"]


def get_numeric_input(prompt: str) -> float:
    """Helper to validate numeric input"""
    while True:
        value = input(f"{prompt}")
        try:
            return float(value)
        except ValueError:
            print(f"❌ Invalid number, please enter a valid value for {prompt}.")


def close_trade(trade_id: int, exit_price: float, notes: str = ""):
    trades = load_trades()

    for t in trades:
        if t["id"] == trade_id and t["status"] == "open":
            quantity = t.get("quantity", 0)
            order_value = t.get("order_value", quantity * t.get("entry", 0))

            # Gross PnL (long vs short)
            if t["direction"] == "long":
                gross_pnl = (exit_price - t["entry"]) * quantity
            else:  # short
                gross_pnl = (t["entry"] - exit_price) * quantity

            # Fees
            entry_fee = t["order_value"] * FEE_RATES["taker"]
            exit_fee = (quantity * exit_price) * FEE_RATES["taker"]
            total_fee = entry_fee + exit_fee

            net_pnl = gross_pnl - total_fee

            # Update trade record
            t.update(
                {
                    "status": "closed",
                    "exit_price": exit_price,
                    "gross_pnl": gross_pnl,
                    "fees_paid": total_fee,
                    "net_pnl": net_pnl,
                    "notes": notes,
                }
            )
            save_trades(trades)
            return t
    return None


def delete_trade(trade_id: int) -> bool:
    """Delete a trade by ID from storage.
    Returns True if deleted, False if not found.
    """
    trades = load_trades() or []
    updated_trades = [t for t in trades if t["id"] != trade_id]

    if len(updated_trades) == len(trades):
        return False  # No trade found to delete

    # reassign IDs to maintain sequence
    for index, trade in enumerate(updated_trades, start=1):
        trade["id"] = index

    save_trades(updated_trades)
    return True


def view_history():
    trades = load_trades()
    if not trades:
        console.print("[red]No trade history found.[/red]")
        return

    # Analytics summary
    closed_trades = [t for t in trades if t["status"] == "closed"]
    total_pnl = sum(t.get("net_pnl", 0) for t in closed_trades)
    total_trades = len(trades)
    win_trades = sum(1 for t in closed_trades if t.get("net_pnl", 0) > 0)
    win_rate = (win_trades / len(closed_trades) * 100) if closed_trades else 0

    console.print("\n[bold cyan]Trade Analytics[/bold cyan]")
    console.print(f"Total trades: {total_trades}")
    console.print(f"Closed trades: {len(closed_trades)}")
    console.print(f"Net PnL: {total_pnl:.2f} USDT")
    console.print(f"Win rate: {win_rate:.2f}%\n")

    # Color-coded history table
    table = Table(title="Trade History", box=box.ROUNDED)
    table.add_column("ID", style="cyan", justify="center")
    table.add_column("Pair", style="magenta")
    table.add_column("Dir", justify="center")
    table.add_column("Status", justify="center")
    table.add_column("Entry")
    table.add_column("Exit")
    table.add_column("Net PnL", justify="right")
    table.add_column("Notes")

    for t in trades:
        pnl = t.get("net_pnl")
        if pnl is None:
            pnl_str = "-"
        elif pnl >= 0:
            pnl_str = f"[green]{pnl:.2f}[/green]"
        else:
            pnl_str = f"[red]{pnl:.2f}[/red]"

        table.add_row(
            str(t["id"]),
            t["pair"],
            t["direction"].upper(),
            t["status"],
            str(t["entry"]),
            str(t.get("exit_price") or "-"),
            pnl_str,
            str(t.get("notes") or "-"),
        )
    console.print(table)
