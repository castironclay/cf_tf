import yaml
from time import sleep
from httpx import Client


def read_creds_file():
    with open("keys.yaml", "r") as creds_file:
        all_creds = yaml.safe_load(creds_file)

    return all_creds


def build_sessions() -> list[dict]:
    sessions: list = []
    creds = read_creds_file()
    for account in creds.keys():
        details = creds.get(account)
        session_info: dict = {}
        btoken = creds.get(account).get("key")
        bearer = f"Bearer {btoken}"
        auth = {"Authorization": bearer}

        s = Client()

        s.headers.update({"Accept": "application/vnd.github+json"})
        s.headers.update({"X-GitHub-Api-Version": "2022-11-28"})
        s.headers.update(auth)
        session_info["session"] = s
        session_info["details"] = details

        sessions.append(session_info)

    return sessions


if __name__ == "__main__":
    sessions = build_sessions()
    for session in sessions:
        account = session.get("details")
        start = f'https://api.github.com/repos/{account.get("account")}/{account.get("repo")}/actions/workflows/{account.get("file")}/dispatches'
        running = f'https://api.github.com/repos/{account.get("account")}/{account.get("repo")}/actions/runs?status=in_progress'
        s = session.get("session")
        try:
            s.post(start, data='{"ref": "main"}')
        except Exception as e:
            print(e)
            quit()
        print("Starting workflow...")
        sleep(3)
        total_count = 0
        # Check until we see a workflow in progress
        while total_count == 0:
            active_workflow = s.get(running)
            output = active_workflow.json()
            total_count = output.get("total_count")
            sleep(1)
