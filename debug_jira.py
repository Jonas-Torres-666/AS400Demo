import requests
from requests.auth import HTTPBasicAuth
import json
import os

def load_env():
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value

load_env()
EMAIL = os.environ.get("JIRA_EMAIL")
TOKEN = os.environ.get("JIRA_TOKEN")
DOMAIN = os.environ.get("JIRA_DOMAIN", "demoia.atlassian.net")

url = f"https://{DOMAIN}/rest/api/3/issue/AS400DEMO-2"
auth = HTTPBasicAuth(EMAIL, TOKEN)
headers = {"Accept": "application/json"}

response = requests.request("GET", url, headers=headers, auth=auth)
if response.status_code == 200:
    print(json.dumps(response.json(), indent=2))
else:
    print(response.text)
