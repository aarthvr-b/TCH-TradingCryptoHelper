from datetime import datetime
from rich.console import Console
from rich import box
from rich.table import Table
from calculator import calculate_position
from storage import load_trades, save_trades

console = Console()
FEE_RATES = {"maker": 0.0002, "taker": 0.00055}


def get_numeric_input(prompt, type_func=float, min_value=None):
    """Helper to validate numeric input"""
    while True:
        try:
            value = type_func(input(prompt))
            if min_value is not None and value < min_value:
                console.print(f"[red]Value must be >= {min_value}[/red]")
                continue
            return value
        except ValueError:
            console.print("[red]Invalid number. Try again.[/red]")


def open_trade():
    trades = load_trades()
    console.print("\n[bold cyan]Open New Trade[/bold cyan]\n")

    # Inputs
    pair = input("Enter trading pair (e.g. BTCUSDT): ")
    account_size = get_numeric_input("Enter account size (USDT): ", float, 0.01)
    risk_pct = get_numeric_input("Enter risk % (e.g. 1-3: )", float, 0.01)
    entry = get_numeric_input("Enter entry price: ", float, 0.0001)
    stop_loss = get_numeric_input("Enter stop loss: ", float, 0.0001)
    direction = input("Direction (long/short): ").strip().lower()
    if direction not in ("long", "short"):
        console.print("[red]Invalid direction. Must be 'long' or 'short'.[/red]")
        return 

    results = calculate_position(account_size, risk_pct, entry, stop_loss)

    # Show summary for confirmation
    console.print("\n[bold yellow]Please confirm your trade: [/bold yellow]")
    console.print(f"Pair: {pair}")
    console.print(f"Direction: {direction.upper}")
    console.print(f"Entry: {entry}")
    console.print(f"Stop Loss: {stop_loss}")
    console.print(f"Position Size: {results['position_size']:.4f}")
    console.print(f"Required Leverage: {results['required_leverage']:.2f}x")
    console.print(f"Risk Amount: {results['risk_amount']:.2f} USDT")
    console.print(f"Estimated Entry Fee (taker): {results['taker_fee']:.2f} USDT")

    confirm = input("\nConfirm trade? (y/n): ").strip().lower()
    if confirm != "y":
        console.print("[red]Trade cancelled.[/red]")
        return

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

    console.print(
        f"\n[bold green]Trade opened:[/bold green] {pair} | "
        f"Dir: {direction.upper()} | "
        f"Size: {results['position_size']:.4f} | "
        f"Lev: {results['required_leverage']:.2f}x | "
        f"Risk: {results['risk_amount']:.2f} USDT"
    )


def close_trade():
    trades = load_trades()
    open_trades = [t for t in trades if t["status"] == "open"]

    if not open_trades:
        console.print("[red]No open trades found.[/red]")
        return

    console.print("[bold cyan]Close Trade[/bold cyan]\n")
    for t in open_trades:
        console.print(
            f"[{t['id']} {t['pair']} | {t['direction']} | "
            f"Entry: {t['entry']} | SL: {t['stop_loss']})]"
        )

    trade_id = int(input("Enter trade ID to close: "))
    exit_price = float(input("Enter exit price: "))
    notes = input("Notes (optional): ")

    for t in trades:
        if t["id"] == trade_id and t["status"] == "open":
            position_size = t["position_size"]

            # Gross PnL (long vs short)
            if t["direction"] == "long":
                gross_pnl = (exit_price - t["entry"]) * position_size
            else:  # short
                gross_pnl = (t["entry"] - exit_price) * position_size

            # Fees
            entry_fee = t["order_value"] * FEE_RATES["taker"]
            exit_fee = (position_size * exit_price) * FEE_RATES["taker"]
            total_fee = entry_fee + exit_fee

            net_pnl = gross_pnl - total_fee
            # Update trade record
            t["status"] = "closed"
            t["exit_price"] = exit_price
            t["gross_pnl"] = gross_pnl
            t["fees_paid"] = total_fee
            t["net_pnl"] = net_pnl
            t["notes"] = notes
            break

    save_trades(trades)
    console.print("[bold green] Trade closed and updates with fees![/bold green]")


def view_history():
    trades = load_trades()
    if not trades:
        console.print("[red]No trade history found.[/red]")
        return

    # Analytics summary 
    closed_trades = [t for t in trades if t["status"] == "closed"]
    total_pnl = sum(t.get("net_pnl",0) for t in closed_trades)
    total_trades = len(trades)
    win_trades = sum(1 for t in closed_trades if t.get("net_pnl", 0) > 0)
    win_rate = (win_trades / len(closed_trades *100 ) if closed_trades else 1)

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
