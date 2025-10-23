from textual.screen import Screen
from textual.widgets import Button, Label, ListItem, ListView

from screens.input_exit_data_screen import InputExitDataScreen
from screens.popup_message import PopupMessage


class CloseTradeScreen(Screen):
    """Screen to close an existing trade."""

    BINDINGS = [("b", "back", "Back")]

    def compose(self):
        self.list_view = ListView()
        yield self.list_view
        yield Button("Select Trade to Close", id="select")
        yield Button("Back", id="back")

    def on_mount(self):
        self.refresh_trades()

    def on_resume(self) -> None:
        self.refresh_trades()

    def refresh_trades(self):
        """Load the latest trades and repopulate the list view."""
        from core.trades import get_open_trades

        self.open_trades = get_open_trades()
        self.list_view.clear()

        if not self.open_trades:
            self.list_view.append(ListItem(Label("No open trades found.")))
            return

        for t in self.open_trades:
            label = f"[{t['id']}] {t['pair']} {t['direction'].upper()} @ {t['entry']}"
            self.list_view.append(ListItem(Label(label)))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "select":
            trade_index = self.list_view.index
            if trade_index is None:
                self.mount(
                    PopupMessage(
                        "❌ No trade selected.",
                        style="bold white on red",
                        auto_close=3,
                    )
                )
                return
            trade = self.open_trades[trade_index]
            self.app.push_screen(InputExitDataScreen(trade))
        elif event.button.id == "back":
            self.app.pop_screen()
