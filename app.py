import sys

from flask import Flask, request
from datetime import datetime
import requests
import os


app = Flask(__name__)

# For security GitHib token is set an environment variable
github_token = os.environ['GITHUB_TOKEN']

# Warning message to set github token
if github_token is None:
    print("Set GITHUB_TOKEN as environment variable")
    sys.exit(-1)


# TODO change hook name
@app.route('/json-example', methods=['POST'])
def json_example():
    request_data = request.get_json()

    api_url = "http://localhost:2000/catalogue-timeline/insert"
    action = request_data.get('action')
    pr = request_data.get('pull_request')

    diff_url = None
    merged = None
    if pr is not None:
        merged = pr.get('merged')
        diff_url = pr.get('url')
        base = pr.get('base')
        repo = base.get('repo')
        repo_name = repo.get('name')
        print(repo_name)


        diff = download_diff(diff_url, github_token)

        files_changed = parse_diff(diff)

        for file in files_changed:
            requests.post(url=api_url, json=payload(file, repo_name))
        return "Ok"

    return "Ok"


def download_diff(url, token):
    headers = {"Authorization": "token {}".format(token),  'Accept': 'application/vnd.github.v3.diff'}
    resp = requests.get(url, headers=headers, allow_redirects=True)
    if resp.status_code == 200:
        print("Diff Downloaded Ok: Diff Content is {}".format(resp.text))
        return resp.text
    else:
        print("Downloading Diff Failed {}".format(resp.status_code))
        print(resp.text)
        return None


def parse_diff(diff):
    files = []
    lines = diff.splitlines()
    print(lines)

    for line in lines:
        #
        if line.startswith("+++ b/") and line.endswith(".conf"):
            files.append(line[6:-5])
    return files

'''
POST       /insert   uk.gov.hmrc.cataloguetimeline.controllers.TimelineAPIController.insertEvent()
service
date "2021-11-15T12:15:19.507Z"
environment
eventType
message
url (optional)'''


def payload(file, repo_name):
    now = datetime.now()

    api_data = {
        "service": file,
        "date": now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        "environment": str(get_environment(repo_name)),
        "eventType": "config-update",
        "message": "Successfully Sent POST Request!"
    }
    return api_data


# TODO update names to fit with repo names for each environment
def get_environment(repo_name):
    environment_lookup = {
        "ConfigUpdate": "production",
        "app-config-qa": "qa-and-build",
        "app-config-external-test": "external-test",
        "app-config-development": "development",
        "app-config-staging": "staging",
        "app-config-integration": "integration"
    }

    return environment_lookup.get(repo_name)


if __name__ == '__main__':
    app.run()
