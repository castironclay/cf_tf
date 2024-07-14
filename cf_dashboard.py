from textual.screen import Screen
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, Grid
from textual.widgets import Footer, Header, Static, Button, Input, Label
from cloudflare import list, create_warp, create_cfd
from rich.console import Console

console = Console()
TEXT = """I must not fear.
Fear is the mind-killer.
Fear is the little-death that brings total obliteration.
I will face my fear.
I will permit it to pass over me and through me.
And when it has gone past, I will turn the inner eye to see its path.
Where the fear has gone there will be nothing. Only I will remain."""


class QuitScreen(Screen):
    """Screen with a dialog to quit."""

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Are you sure you want to quit?", id="question"),
            Button("Quit", variant="error", id="quit"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.exit()
        else:
            self.app.pop_screen()


class CfTunnelApp(App):
    BINDINGS = [
        Binding(key="ctrl+c", action="quit", description="Quit the app"),
        Binding(key="ctrl+r", action="refresh", description="Refresh"),
        Binding(
            key="question_mark",
            action="help",
            description="Show help screen",
            key_display="?",
        ),
    ]
    CSS_PATH = "styles.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        WARP = Static(list("warp"), id="list_warp")
        WARP.border_title = "Warp Tunnels"

        CFD = Static(list("cfd"), id="list_cfd")
        CFD.border_title = "CFD Tunnels"

        yield Horizontal(
            Vertical(
                Input(
                    placeholder="New tunnel name",
                    type="text",
                    tooltip="Name for tunnel",
                    id="warp_input",
                ),
                Button("Delete", id="delete_warp"),
                WARP,
                Input(
                    placeholder="New tunnel name",
                    type="text",
                    tooltip="Name for tunnel",
                    id="cfd_input",
                ),
                Button("Delete", id="delete_cfd"),
                CFD,
                classes="column",
                id="action_buttons",
            ),
            Vertical(Static("Details"), Static("Details"), classes="column"),
        )
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Cloudflare"
        self.sub_title = "Zero Trust Tunnels"

    def on_input_submitted(self, event: Input.Submitted) -> None:
        input_id = event.input.id
        value = event.input.value
        if input_id == "warp_input":
            create_warp(value)
            event.input.clear()
            self.notify("WARP tunnel created", severity="success", timeout=10)
            self.query_one("#list_warp").update(list("warp"))

        if input_id == "cfd_input":
            create_cfd(value)
            event.input.clear()
            self.notify("Cloudflared tunnel created", severity="success", timeout=10)
            self.query_one("#list_cfd").update(list("cfd"))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        pass

    # def action_refresh(self):
    #     self.notify("Refreshed", severity="success", timeout=1)
    #     self.query_one("#list_warp").update(list("warp"))
    #     self.query_one("#list_cfd").update(list("cfd"))
    def action_refresh(self) -> None:
        self.push_screen(QuitScreen())


if __name__ == "__main__":
    app = CfTunnelApp()
    app.run()
