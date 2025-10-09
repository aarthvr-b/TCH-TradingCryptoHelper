from textual.screen import Screen
from textual.widgets import Button, Input, Static

from core.trades import open_trade
from screens.popup_message import PopupMessage


class OpenTradeScreen(Screen):
    """Screen to open a new trade."""

    BINDINGS = [("b", "back", "Back")]

    def compose(self):
        yield Static("📈 Open Trade\nFill in the details below:")

        # Text inputs
        self.pair_input = Input(placeholder="Pair (e.g. BTCUSDT)")
        self.account_input = Input(placeholder="Account Size (USDT)")
        self.risk_input = Input(placeholder="Risk % (1-3)")
        self.entry_input = Input(placeholder="Entry Price")
        self.dir_input = Input(placeholder="Trade direction (long/short)")
        self.stop_input = Input(placeholder="Stop Loss")

        yield self.pair_input
        yield self.account_input
        yield self.risk_input
        yield self.entry_input
        yield self.stop_input
        yield self.dir_input

        yield Button("Submit", id="submit")
        yield Button("Back", id="back")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit":
            try:
                trade = open_trade(
                    pair=self.pair_input.value.strip().upper(),
                    direction=self.dir_input.value.strip().lower(),
                    account_size=float(self.account_input.value),
                    risk_pct=float(self.risk_input.value),
                    entry=float(self.entry_input.value),
                    stop_loss=float(self.stop_input.value),
                )

                lev = trade["required_leverage"]
                if lev <= 3:
                    style = "bold white on green"
                elif 3 < lev <= 10:
                    style = "bold black on yellow"
                else:
                    style = "bold white on red"

                # Build summary message
                msg = (
                    f"\n\n✅ Trade added to the list, input the following Quantity\n\n"
                    f"Pair: {trade['pair']} ({trade['direction'].upper()})\n"
                    f"Quantity: {trade['quantity']:.4f}\n"
                    f"Order value: {trade['order_value']:.2f} USDT\n"
                    f"Required Leverage: {lev:.1f}x"
                    f"Risk per trade: {trade['risk_amount']:.2f} USDT\n"
                    f"{trade['leverage_note']}\n\n"
                    f"Fees → Maker: {trade['maker_fee']:.4f} | Taker: {trade['taker_fee']:.4f}"
                )

                self.mount(PopupMessage(msg, style=style))
            except ValueError as e:
                self.mount(
                    PopupMessage(
                        f"❌ Invalid input: {e}",
                        style="bold white on red",
                    )
                )
        elif event.button.id == "back":
            self.app.pop_screen()
