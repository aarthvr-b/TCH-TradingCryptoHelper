from textual import events
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Label, ListItem, ListView, Static

from screens import CloseTradeScreen, OpenTradeScreen, ViewHistoryScreen


class CryptoHelperApp(App):
    CSS_PATH = None

    MENU_ITEMS = [
        "Open Trade",
        "Close Trade",
        "View History",
        "Exit",
    ]

    MENU_MAP = {
        0: OpenTradeScreen,
        1: CloseTradeScreen,
        2: ViewHistoryScreen,
        3: exit,
    }

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Static(
            "👋 Welcome to TCH - Trading Crypto Helper\n\n"
            "Use ↑/↓ or type the number to select."
        )

        self.menu = ListView(*[ListItem(Label(item)) for item in self.MENU_ITEMS])
        yield self.menu

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle arrow-key selection + Enter"""
        index = self.menu.index
        if index is None:
            return
        choice = self.MENU_MAP.get(index)
        if choice == "exit":
            self.exit()
        elif choice:
            self.push_screen(choice())

    def on_key(self, event: events.Key) -> None:
        """Handle number keys and quit shortcut."""
        if event.key == "q":
            self.exit()
        elif event.key == "b":
            # Pop all screens back to the root menu
            while len(self.screen_stack) > 1:
                self.pop_screen()
        elif event.key in [str(i + 1) for i in range(len(self.MENU_ITEMS))]:
            self.handle_menu_choice(
                f"[{event.key}] {self.MENU_ITEMS[int(event.key) - 1]}"
            )

    def handle_menu_choice(self, choice: str) -> None:
        """Run the logic for each menu option."""
        screen_maps = {
            "[1] Open Trade": OpenTradeScreen,
            "[2] Close Trade": CloseTradeScreen,
            "[3] View History": ViewHistoryScreen,  #
            "exit": self.exit,
        }
        if choice in screen_maps:
            screen_maps[choice]()


if __name__ == "__main__":

    app = CryptoHelperApp()
    app.run()
