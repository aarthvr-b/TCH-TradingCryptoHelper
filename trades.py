from datetime import datetime
from rich.console import Console
from rich import box
from rich.table import Table
from calculator import calculate_position
from storage import load_trades, save_trades

console = Console()
FEE_RATES = {"maker": 0.0002, "taker": 0.00055}


def open_trade():
    trades = load_trades()
    console.print("[bold cyan]Open New Trade[/bold cyan]\n")

    # Inputs
    pair = input("Enter trading pair (e.g. BTCUSDT): ")
    account_size = float(input("Enter account size (USDT): "))
    risk_pct = float(input("Enter risk % (e.g. 1-3: )"))
    entry = float(input("Enter entry price: "))
    stop_loss = float(input("Enter stop loss: "))
    direction = input("Direction (long/short): ").strip().lower()

    results = calculate_position(account_size, risk_pct, entry, stop_loss)
    
    # Show summary for confirmation
    console.print("\n[bold yellow]Please confirm your trade: [/bold yellow]")
    console.print(f"Pair: {pair}")
    console.print(f"Direction: {direction.upper}")
    console.print(f"Entry: {entry}")
    console.print(f"Stop Loss: {stop_loss}")

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
            else: # short
                gross_pnl = (t["entry"] - exit_price) * position_size

            #Fees
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
            str(t.get("notes") or "-")
        )
    console.print(table)
