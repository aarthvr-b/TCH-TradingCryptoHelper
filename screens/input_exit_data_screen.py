from textual.screen import Screen
from textual.widgets import Button, Input, Static

from core.trades import close_trade
from screens.popup_message import PopupMessage


class InputExitDataScreen(Screen):
    """Screen to enter exit data for closing a trade."""

    def __init__(self, trade):
        super().__init__()
        self.trade = trade

    def compose(self):
        yield Static(
            f"📉 Closing Trade ID {self.trade['id']} - {self.trade['pair']} {self.trade['direction'].upper()} @ {self.trade['entry']}"
        )
        self.exit_input = Input(placeholder="Exit Price")
        self.notes_input = Input(placeholder="Notes (optional)")
        yield self.exit_input
        yield self.notes_input
        yield Button("Submit", id="submit")
        yield Button("Back", id="back")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit":
            try:
                exit_price = float(self.exit_input.value)
                notes = self.notes_input.value.strip() or ""

                closed_trade = close_trade(
                    trade_id=self.trade["id"], exit_price=exit_price, notes=notes
                )

                if closed_trade:
                    pnl = closed_trade.get("pnl", 0)
                    gross = closed_trade.get("gross_pnl", 0)
                    fees = closed_trade.get("fees_paid", 0)

                    if pnl > 0:
                        style = "bold white on green"
                        emoji = "🚀"
                        result_text = f"Profitable trade!: +${pnl:.2f} (Gross: +${gross:.2f}, Fees: -${fees:.2f})"
                    elif pnl < 0:
                        style = "bold white on red"
                        emoji = "💀"
                        result_text = f"Losing trade: -${-pnl:.2f} (Gross: -${-gross:.2f}, Fees: -${fees:.2f})"
                    else:
                        style = "bold white on yellow"
                        emoji = "😐"
                        result_text = f"Breakeven trade: $0.00 (Gross: ${gross:.2f}, Fees: -${fees:.2f})"

                    # --- Summary Message ---
                    msg = (
                        f"{emoji} {result_text}\n\n"
                        f"Pair: {closed_trade['pair']} ({closed_trade['direction'].upper()})\n"
                        f"Entry: {closed_trade['entry']:.4f}\n"
                        f"Exit: {closed_trade['exit_price']:.4f}\n"
                        f"Quantity: {closed_trade.get('quantity', '-')}\n\n"
                        f"Gross PnL: {gross:.2f} USDT\n"
                        f"Fees Paid: {fees:.2f} USDT\n"
                        f"Net PnL: {pnl:.2f} USDT\n\n"
                        f"{'🟢 Well done!' if pnl > 0 else '🔴 Review your Strategies.' if pnl < 0 else '🟡 Flat outcome — good discipline!'}"
                    )

                    popup = PopupMessage(msg, style=style, auto_close=None)
                    self.mount(popup)

                    # def return_to_menu():
                    #     self.app.pop_screen()  # Pop the popup message
                    #     self.app.pop_screen()  # Return to menu

                    # popup.set_timer(0.2, return_to_menu)

                else:
                    self.mount(
                        PopupMessage(
                            "❌ Trade not found.",
                            style="bold white on red",
                            auto_close=3,
                        )
                    )
            except ValueError as e:
                self.mount(
                    PopupMessage(
                        f"❌ Invalid input: {e}",
                        style="bold white on red",
                        auto_close=3,
                    )
                )
        elif event.button.id == "back":
            self.app.pop_screen()
