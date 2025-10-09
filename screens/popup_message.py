# screens/ popup_message.py
from rich.text import Text
from textual.containers import Container
from textual.events import Mount
from textual.widget import Widget
from textual.widgets import Button, Static


class PopupMessage(Widget):
    """Reusable popup message for TUI apps."""

    def __init__(
        self,
        message: str,
        style: str = "white on dark_blue",
        auto_close: float | None = 0,
        **kwargs
    ):
        """
        Args:
            :param message: The Text to show
            :param style: Rich style string for the message
            :param auto_close: Time in second to auto-close. 0 or None disables it
        """
        super().__init__(**kwargs)
        self.message_text = message
        self.message_style = style
        self.auto_close = auto_close
        self.container = None

    def compose(self):
        """
        The container holds the message and close button
        """
        self.container = Container(
            Static(Text(self.message_text, style=self.message_style), expand=True),
            Button("Close", id="popup_close"),
            id="popup_container",
        )
        yield self.container

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "popup_close":
            self.remove()

    def on_mount(self):
        if self.auto_close and self.auto_close > 0:
            # Automatically remove after timer
            self.set_timer(self.auto_close, self.remove)
