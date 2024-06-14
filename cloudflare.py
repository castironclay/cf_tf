import json

import typer
import yaml
from requests import Session, session

app = typer.Typer()


@app.callback()
def callback():
    """
    Cloudflare Tunnels.\n
    Interact with Cloudflare WARP Tunnels.\n
    """


def read_creds_file() -> dict:
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


@app.command()
def view():
    """
    View existing WARP connectors
    """
    s, creds = build_session()

    response = s.get(
        f"https://api.cloudflare.com/client/v4/accounts/{creds.get('account_id')}/warp_connector",
    )

    if response.status_code != 200:
        print(json.dumps({"status": str(response.status_code), "msg": response.reason}))
        return

    print(json.dumps(response.json()))


@app.command()
def delete():
    """
    Delete WARP connector
    """
    s, creds = build_session()
    with open("tunnel.json", "r") as openfile:
        json_object = json.load(openfile)

    tunnel_id = json_object.get("id")

    response = s.delete(
        f"https://api.cloudflare.com/client/v4/accounts/{creds.get('account_id')}/warp_connector/{tunnel_id}",
        data='{"name": "testing"}',
    )

    if response.status_code != 200:
        print(json.dumps({"status": str(response.status_code), "msg": response.reason}))
        return


    print(json.dumps({"TunnelName": "None", "TunnelSecret": "None"}))


@app.command()
def create():
    """
    Create WARP connector
    """
    s, creds = build_session()

    response = s.post(
        f"https://api.cloudflare.com/client/v4/accounts/{creds.get('account_id')}/warp_connector",
        data='{"name": "testing"}',
    )

    if response.status_code != 200:
        print(json.dumps({"status": str(response.status_code), "msg": response.reason}))
        return

    data = json.loads(response.content)

    with open("tunnel.json", "w") as outfile:
        data_for_file = json.dumps(data.get("result"))
        outfile.write(data_for_file)

    print(
        json.dumps(
            {
                "TunnelName": data.get("result")
                .get("credentials_file")
                .get("TunnelName"),
                "TunnelSecret": data.get("result")
                .get("credentials_file")
                .get("TunnelSecret"),
            }
        )
    )


if __name__ == "__main__":
    app()
