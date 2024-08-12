import yaml
from time import sleep
from httpx import Client
import io
import zipfile


def read_creds_file():
    with open("keys.yaml", "r") as creds_file:
        all_creds = yaml.safe_load(creds_file)

    return all_creds


class Workflow:
    def __init__(self, account_details):
        self.details = account_details
        self.session = self.build_session(self.details)

    def build_session(self, creds):
        btoken = creds.get("key")
        bearer = f"Bearer {btoken}"
        auth = {"Authorization": bearer}

        s = Client()
        s.headers.update({"Accept": "application/vnd.github+json"})
        s.headers.update({"X-GitHub-Api-Version": "2022-11-28"})
        s.headers.update(auth)

        return s

    def start_workflow(self):
        details = self.details
        start = f'https://api.github.com/repos/{details.get("account")}/{details.get("repo")}/actions/workflows/{details.get("file")}/dispatches'
        s = self.session
        s.post(start, data='{"ref": "main"}')

    def check_running(self):
        details = self.details
        running = f'https://api.github.com/repos/{details.get("account")}/{details.get("repo")}/actions/runs?status=in_progress'
        s = self.session
        total_count = 0

        # Check until we see a workflow in progress
        while total_count == 0:
            active_workflow = s.get(running)
            output = active_workflow.json()
            total_count = output.get("total_count")

        active_workflow = s.get(running)
        self.workflow_details = active_workflow.json()

    def cancel_workflow(self):
        details = self.details
        workflow_details = self.workflow_details
        workflow_id = workflow_details.get("workflow_runs")[0].get("id")
        cancel = f"https://api.github.com/repos/{details.get("account")}/{details.get("repo")}/actions/runs/{workflow_id}/cancel"
        s = self.session
        s.post(cancel)

    def get_workflow_logs(self):
        details = self.details
        workflow_details = self.workflow_details
        workflow_id = workflow_details.get("workflow_runs")[0].get("id")
        get_logs = f"https://api.github.com/repos/{details.get("account")}/{details.get("repo")}/actions/runs/{workflow_id}/logs"
        s = self.session

        # Seems like it takes a bit for the logs to be available so this will try until we get a 200
        cloudflared_url = False
        status_code = 404
        while status_code != 200:
            logs = s.get(get_logs, follow_redirects=True)
            status_code = logs.status_code
            print("Not 200 yet")
            sleep(3)

        while not cloudflared_url:
            download_url = logs.request.url
            # Build fresh client without any special headers and download our logs zip
            # A pre-signed URL is used so we dont need to worry about authentication
            new_client = Client()
            download_file = new_client.get(download_url)

            print("checking logs")
            content = download_file.content
            try:
                zip_file_io = io.BytesIO(content)

                # Open the zip file from the BytesIO object
                with zipfile.ZipFile(zip_file_io) as zf:
                    # Iterate through the files in the zip archive
                    for file_name in zf.namelist():
                        # Read the file content into memory
                        if "cloudflared" in file_name:
                            with zf.open(file_name) as file:
                                file_content = file.readlines()
                                for line in file_content:
                                    line = line.decode()
                                    if ".trycloudflare.com" in line:
                                        print(
                                            f'Your URL is: {line.split("|")[1].strip()}'
                                        )
                                        cloudflared_url = True

            except zipfile.BadZipFile:
                # Will hit this error if we haven't gotten our zip file yet
                sleep(3)
                print("zip error")
                continue

            sleep(3)


if __name__ == "__main__":
    creds = read_creds_file()
    for account in creds.keys():
        details = creds.get(account)
        work = Workflow(details)
        work.start_workflow()
        work.check_running()
        print("workflow started")
        # Sleep for 10 seconds before getting logs
        # Could maybe grab logs repeatedly until we get the ones we want
        sleep(10)
        work.get_workflow_logs()

        sleep(1)
        print("workflow cancelled")
        work.cancel_workflow()
