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

url = f"https://{DOMAIN}/rest/api/3/search/jql"
auth = HTTPBasicAuth(EMAIL, TOKEN)
headers = {"Accept": "application/json"}

# Search for all stories assigned to me
query = {
    "jql": "issuetype = Story AND assignee = currentUser()",
    "fields": "summary,status,key,issuetype,parent"
}

response = requests.request("GET", url, headers=headers, params=query, auth=auth)
if response.status_code == 200:
    data = response.json()
    issues = data.get("issues", [])
    if not issues:
        print("No user stories assigned to you were found.")
    else:
        print(f"{'Key':<12} | {'Summary':<40} | {'Status':<12} | {'Epic'}")
        print("-" * 100)
        for issue in issues:
            fields = issue.get("fields", {})
            key = issue.get("key")
            summary = fields.get("summary", "No Summary")
            status = fields.get("status", {}).get("name", "Unknown")
            parent = fields.get("parent", {})
            epic = parent.get("fields", {}).get("summary", "None") if parent else "None"
            print(f"{key:<12} | {summary:<40} | {status:<12} | {epic}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
