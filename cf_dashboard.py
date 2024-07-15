from textual.screen import Screen
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, Grid
from textual.widgets import Footer, Header, Static, Button, Input, Label
from cf_commands import list, create_warp, create_cfd, delete_warp, delete_cfd
import pyperclip


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


class NewCFDTunnel(Screen):
    """Screen with pastable"""

    def compose(self) -> ComposeResult:
        yield Grid(
            Input(
                placeholder="New tunnel name",
                type="text",
                tooltip="Name for tunnel",
                id="cfd_input",
            ),
            Button("Done", variant="primary", id="done"),
            Static(id="download_link"),
            id="dialog",
        )

    def on_input_submitted(self, event: Input.Submitted) -> None:
        value = event.input.value
        download_link = create_cfd(value)
        event.input.clear()
        self.notify("Cloudflared tunnel created", severity="success", timeout=3)
        self.query_one("#download_link").update(download_link)
        pyperclip.copy(download_link)
        self.notify("Link copied to clipboard", severity="success", timeout=10)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.pop_screen()


class NewWarpTunnel(Screen):
    """Screen with pastable"""

    def compose(self) -> ComposeResult:
        yield Grid(
            Input(
                placeholder="New tunnel name",
                type="text",
                tooltip="Name for tunnel",
                id="warp_input",
            ),
            Button("Done", variant="primary", id="done"),
            id="dialog",
        )
        yield Static(id="download_link")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        value = event.input.value
        download_link = create_warp(value)
        event.input.clear()
        self.notify("Warp tunnel created", severity="success", timeout=3)
        self.query_one("#download_link").update(download_link)
        pyperclip.copy(download_link)
        self.notify("Link copied to clipboard", severity="success", timeout=10)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "done":
            self.app.pop_screen()
        else:
            self.app.pop_screen()


class DeleteWarpTunnel(Screen):
    """Screen with pastable"""

    def compose(self) -> ComposeResult:
        yield Grid(
            Input(
                placeholder="Tunnel name",
                type="text",
                tooltip="Name of tunnel",
                id="warp_input",
            ),
            Button("Done", variant="primary", id="done"),
            id="dialog",
        )

    def on_input_submitted(self, event: Input.Submitted) -> None:
        value = event.input.value
        delete_warp(value)
        event.input.clear()
        self.notify("Warp tunnel deleted", severity="success", timeout=3)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "done":
            self.app.pop_screen()
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

        yield Vertical(
            Button("Create", id="create_warp"),
            Button("Delete", id="delete_warp"),
            WARP,
            Button("Create", id="create_cfd"),
            Button("Delete", id="delete_cfd"),
            CFD,
            classes="column",
            id="action_buttons",
        )
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Cloudflare"
        self.sub_title = "Zero Trust Tunnels"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "create_warp":
            self.push_screen(NewWarpTunnel())

        if event.button.id == "delete_warp":
            self.push_screen(DeleteWarpTunnel())

        if event.button.id == "create_cfd":
            self.push_screen(NewCFDTunnel())

        if event.button.id == "delete_cfd":
            self.push_screen(DeleteCFDTunnel())

    def action_refresh(self):
        self.notify("Refreshed", severity="success", timeout=3)
        self.query_one("#list_warp").update(list("warp"))
        self.query_one("#list_cfd").update(list("cfd"))

    def action_quit(self) -> None:
        self.push_screen(QuitScreen())


if __name__ == "__main__":
    app = CfTunnelApp()
    app.run()
