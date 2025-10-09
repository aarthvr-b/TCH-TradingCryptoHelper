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
                notes = self.notes_input.value.strip() or None
                closed_trade = close_trade(
                    trade_id=self.trade["id"], exit_price=exit_price, notes=notes
                )
                if closed_trade:
                    self.mount(
                        PopupMessage(
                            "✅ Trade closed successfully!",
                            style="bold white on green",
                            auto_close=3,
                        )
                    )
                    self.app.pop_screen()  # Pop EnterExitDataScreen
                    self.app.pop_screen()  # Pop CloseTradeScreen
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
