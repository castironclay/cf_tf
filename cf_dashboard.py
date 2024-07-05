from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import (
    Footer,
    Header,
    Static,
    Button,
    Input,
    ListItem,
    ListView,
    Label,
)
from cloudflare import list, create_warp, create_cfd
from rich.console import Console

console = Console()


class CfTunnelApp(App):
    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
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


if __name__ == "__main__":
    app = CfTunnelApp()
    app.run()
