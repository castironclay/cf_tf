import json
import yaml
import typer
from requests import Session, session
from rich import print as rprint
from rich.console import Console
from rich.table import Table

app = typer.Typer(pretty_exceptions_enable=False)
view_app = typer.Typer()
app.add_typer(view_app, name="view", help="View tunnel details")
delete_app = typer.Typer()
app.add_typer(delete_app, name="delete", help="Delete tunnels")
create_app = typer.Typer()
app.add_typer(create_app, name="create", help="Create tunnels")


@app.callback()
def callback():
    """
    Cloudflare Tunnels.\n
    Interact with Cloudflare WARP Tunnels.\n
    """


def read_creds_file():
    with open("cf_config.yaml", "r") as creds_file:
        all_creds = yaml.safe_load(creds_file)

    return all_creds


def build_session() -> tuple[Session, dict]:
    s = session()
    creds = read_creds_file()

    s.headers.update({"X-Auth-Key": f"{creds.get("api_key")}"})
    s.headers.update({"X-Auth-Email": f"{creds.get("api_email")}"})
    s.headers.update({"Content-Type": "application/json"})

    return s, creds


@view_app.command("cfd")
def view_cfd(
    name: str = typer.Option(None, help="Tunnel name"),
    token: bool = typer.Option(False, help="Display tunnel token"),
):
    """
    View Cloudflared tunnel details
    """
    s, creds = build_session()

    response = s.get(
        f"https://api.cloudflare.com/client/v4/accounts/{creds.get('account_id')}/tunnels",
    )
    all_tunnels = response.json()
    tunnel_id = ""
    for tunnel in all_tunnels.get("result"):
        if tunnel.get("name") == name and tunnel.get("deleted_at") == None:
            tunnel_id = tunnel.get("id")

    tunnel_info = s.get(
        f"https://api.cloudflare.com/client/v4/accounts/{creds.get('account_id')}/cfd_tunnel/{tunnel_id}",
    )

    if tunnel_info.status_code != 200:
        print(
            json.dumps(
                {"status": str(tunnel_info.status_code), "msg": tunnel_info.reason}
            )
        )
        return

    tunnel = tunnel_info.json()
    tunnel_result = tunnel.get("result")

    if token:
        tunnel_token = s.get(
            f"https://api.cloudflare.com/client/v4/accounts/{creds.get('account_id')}/cfd_tunnel/{tunnel_id}/token",
        )

        if tunnel_token.status_code != 200:
            print(
                json.dumps(
                    {
                        "status": str(tunnel_token.status_code),
                        "msg": tunnel_token.reason,
                    }
                )
            )
            return
        tunnel_token = tunnel_token.json()

        tunnel_result["token"] = tunnel_token.get("result")

    rprint(tunnel_result)


@view_app.command("warp")
def view_warp(
    name: str = typer.Option(None, help="Tunnel name"),
    token: bool = typer.Option(False, help="Display tunnel token"),
):
    """
    View WARP tunnel details
    """
    s, creds = build_session()

    response = s.get(
        f"https://api.cloudflare.com/client/v4/accounts/{creds.get('account_id')}/tunnels",
    )
    all_tunnels = response.json()
    tunnel_id = ""
    for tunnel in all_tunnels.get("result"):
        if tunnel.get("name") == name and tunnel.get("deleted_at") == None:
            tunnel_id = tunnel.get("id")

    tunnel_info = s.get(
        f"https://api.cloudflare.com/client/v4/accounts/{creds.get('account_id')}/warp_connector/{tunnel_id}",
    )

    if tunnel_info.status_code != 200:
        print(
            json.dumps(
                {"status": str(tunnel_info.status_code), "msg": tunnel_info.reason}
            )
        )
        return

    tunnel = tunnel_info.json()
    tunnel_result = tunnel.get("result")

    if token:
        tunnel_token = s.get(
            f"https://api.cloudflare.com/client/v4/accounts/{creds.get('account_id')}/warp_connector/{tunnel_id}/token",
        )

        if tunnel_token.status_code != 200:
            print(
                json.dumps(
                    {
                        "status": str(tunnel_token.status_code),
                        "msg": tunnel_token.reason,
                    }
                )
            )
            return
        tunnel_token = tunnel_token.json()

        tunnel_result["token"] = tunnel_token.get("result")

    rprint(tunnel_result)


@app.command()
def list(type: str) -> Table:
    """
    List existing Zero Trust or Cloudflared tunnels
    """
    s, creds = build_session()

    if type == "warp":
        response = s.get(
            f"https://api.cloudflare.com/client/v4/accounts/{creds.get('account_id')}/warp_connector",
        )

        if response.status_code != 200:
            print(
                json.dumps(
                    {"status": str(response.status_code), "msg": response.reason}
                )
            )
            return
        tunnels = response.json()
        table = Table()

    if type == "cfd":
        response = s.get(
            f"https://api.cloudflare.com/client/v4/accounts/{creds.get('account_id')}/cfd_tunnel",
        )

        if response.status_code != 200:
            print(
                json.dumps(
                    {"status": str(response.status_code), "msg": response.reason}
                )
            )
            return
        tunnels = response.json()
        table = Table()

    table.add_column("Name", style="magenta")
    table.add_column("Status", justify="right", style="green")

    for tunnel in tunnels.get("result"):
        if tunnel.get("deleted_at") == None:
            table.add_row(tunnel.get("name"), tunnel.get("status"))

    return table


@delete_app.command("cfd")
def delete_cfd(name: str):
    """
    Delete Cloudflared tunnel
    """
    s, creds = build_session()
    response = s.get(
        f"https://api.cloudflare.com/client/v4/accounts/{creds.get('account_id')}/tunnels",
    )
    all_tunnels = response.json()
    tunnel_id = ""
    for tunnel in all_tunnels.get("result"):
        if tunnel.get("name") == name and tunnel.get("deleted_at") == None:
            tunnel_id = tunnel.get("id")

    response = s.delete(
        f"https://api.cloudflare.com/client/v4/accounts/{creds.get('account_id')}/cfd_tunnel/{tunnel_id}"
    )

    if response.status_code != 200:
        print(json.dumps({"status": str(response.status_code), "msg": response.reason}))
        return

    print(json.dumps({"TunnelName": "None", "TunnelToken": "None"}))


@delete_app.command("warp")
def delete_warp(name: str):
    """
    Delete WARP tunnel
    """
    s, creds = build_session()
    response = s.get(
        f"https://api.cloudflare.com/client/v4/accounts/{creds.get('account_id')}/tunnels",
    )
    all_tunnels = response.json()
    tunnel_id = ""
    for tunnel in all_tunnels.get("result"):
        if tunnel.get("name") == name and tunnel.get("deleted_at") == None:
            tunnel_id = tunnel.get("id")

    response = s.delete(
        f"https://api.cloudflare.com/client/v4/accounts/{creds.get('account_id')}/warp_connector/{tunnel_id}"
    )

    if response.status_code != 200:
        print(json.dumps({"status": str(response.status_code), "msg": response.reason}))
        return

    print(json.dumps({"TunnelName": "None", "TunnelToken": "None"}))


@create_app.command("cfd")
def create_cfd(name: str):
    """
    Create WARP connector
    """
    s, creds = build_session()
    payload = {"name": name}

    payload_json = json.dumps(payload)

    response = s.post(
        f"https://api.cloudflare.com/client/v4/accounts/{creds.get('account_id')}/cfd_tunnel",
        data=payload_json,
    )

    if response.status_code != 200:
        print(json.dumps({"status": str(response.status_code), "msg": response.reason}))
        return

    data = json.loads(response.content)
    print(
        json.dumps(
            {
                "TunnelName": data.get("result")
                .get("credentials_file")
                .get("TunnelName"),
                "TunnelToken": data.get("result").get("token"),
            }
        )
    )


@create_app.command("warp")
def create_warp(name: str):
    """
    Create WARP connector
    """
    s, creds = build_session()
    payload = {"name": name}

    payload_json = json.dumps(payload)

    response = s.post(
        f"https://api.cloudflare.com/client/v4/accounts/{creds.get('account_id')}/warp_connector",
        data=payload_json,
    )

    if response.status_code != 200:
        print(json.dumps({"status": str(response.status_code), "msg": response.reason}))
        return

    data = json.loads(response.content)
    print(
        json.dumps(
            {
                "TunnelName": data.get("result")
                .get("credentials_file")
                .get("TunnelName"),
                "TunnelToken": data.get("result").get("token"),
            }
        )
    )


if __name__ == "__main__":
    app()
