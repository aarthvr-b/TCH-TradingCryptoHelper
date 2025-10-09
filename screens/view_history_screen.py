from textual.screen import Screen
from textual.widgets import Button, DataTable, Static

from core.trades import delete_trade
from screens.popup_message import PopupMessage
from storage import load_trades


class ViewHistoryScreen(Screen):
    """Interactive trade history with row navigation + delete."""

    BINDINGS = [
        ("b", "back", "Back"),
        ("d", "delete_selected", "Delete Selected Trade"),
    ]

    def __init__(self):
        super().__init__()
        self.trades: list[dict] = []
        self.highlighted_row_key: int | None = None

    def compose(self):
        yield Static("📜 Trade History (↑/↓ move • D delete • B back)")
        yield DataTable(id="history_table", zebra_stripes=True)
        yield Button("Back", id="back")

    def on_mount(self):
        table = self.query_one("#history_table", DataTable)
        table.add_columns(
            "ID", "Pair", "Dir", "Status", "Entry", "Exit", "Net PnL", "Notes"
        )

        self._reload_table()

        # Focus and highlight the first row
        table.focus()
        table.cursor_type = "row"  # highlight full row, if supported

        if table.row_count > 0:
            # Some versions return list, others Row; handle both
            try:
                first_key = getattr(table.get_row_at(0), "key", None)
            except Exception:
                # fallback: we stored the trade id as row key earlier
                first_key = (
                    table.get_row_key_at(0)
                    if hasattr(table, "get_row_key_at")
                    else None
                )

            # If nothing else works, use the first trade id in self.trades
            if not first_key and self.trades:
                first_key = int(self.trades[0]["id"])

            if first_key:
                self.highlighted_row_key = first_key
                try:
                    table.move_cursor(row=0, column=0)
                except Exception:
                    pass  # older versions may not have move_cursor()

    def _reload_table(self):
        """Load trades and repopulate DataTable."""
        table = self.query_one("#history_table", DataTable)
        self.trades = load_trades() or []
        table.clear(columns=False)

        if not self.trades:
            table.add_row("-", "No trades found", "-", "-", "-", "-", "-", "-")
            self.highlighted_row_key = None
            return

        for t in self.trades:
            pnl = t.get("net_pnl")
            pnl_str = "-" if pnl is None else f"{pnl:.2f}"
            # We pass key=t["id"], so it can be referenced safely later
            table.add_row(
                str(t["id"]),
                t["pair"],
                t["direction"].upper(),
                t["status"],
                str(t["entry"]),
                str(t.get("exit_price") or "-"),
                pnl_str,
                str(t.get("notes") or "-"),
                key=int(t["id"]),
            )

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted):
        """Track which row is currently highlighted."""
        # Some Textual versions pass the row key directly; others require event.row_key
        self.highlighted_row_key = getattr(event, "row_key", None)

    def action_delete_selected(self):
        """Ask for confirmation before deleting the selected trade."""
        table = self.query_one("#history_table", DataTable)
        trade_id = self.highlighted_row_key

        # Handle versions where row_key is wrapped
        if hasattr(trade_id, "value"):
            trade_id = trade_id.value
        if isinstance(trade_id, str) and trade_id.isdigit():
            trade_id = int(trade_id)

        if not trade_id:
            if self.trades:
                trade_id = int(self.trades[0]["id"])
            else:
                self.mount(
                    PopupMessage(
                        "No trades to delete.", style="bold white on red", auto_close=2
                    )
                )
                return

        self.pending_delete_id = trade_id
        self.mount(
            PopupMessage(
                f"⚠️ Are you sure you want to delete Trade {trade_id}? (Y/N)",
                style="bold white on red",
            )
        )

    def on_key(self, event):
        """Listen for Y/N confirmation when popup is active."""
        if not hasattr(self, "pending_delete_id"):
            return

        key = event.key.lower()
        if key == "y":
            trade_id = self.pending_delete_id
            del self.pending_delete_id

            if delete_trade(int(trade_id)):
                self.mount(
                    PopupMessage(
                        f"✅ Trade {trade_id} deleted successfully.",
                        style="bold white on green",
                        auto_close=2,
                    )
                )
                self._reload_table()
            else:
                self.mount(
                    PopupMessage(
                        f"❌ Trade {trade_id} not found.",
                        style="bold white on red",
                        auto_close=2,
                    )
                )

        elif key == "n":
            del self.pending_delete_id
            self.mount(
                PopupMessage(
                    "❎ Deletion cancelled.",
                    style="bold white on yellow",
                    auto_close=2,
                )
            )

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "back":
            self.app.pop_screen()
