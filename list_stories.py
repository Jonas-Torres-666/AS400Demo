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

# Search for all stories in the project
query = {
    "jql": "issuetype = Story",
    "fields": "summary,status,key,issuetype,parent,assignee"
}

response = requests.request("GET", url, headers=headers, params=query, auth=auth)
if response.status_code == 200:
    data = response.json()
    issues = data.get("issues", [])
    print(f"Found {len(issues)} stories.")
    for issue in issues:
        fields = issue.get("fields", {})
        key = issue.get("key")
        summary = fields.get("summary")
        assignee_data = fields.get("assignee")
        assignee = assignee_data.get("displayName", "Unassigned") if assignee_data else "Unassigned"
        parent = fields.get("parent", {})
        epic = parent.get("fields", {}).get("summary", "None") if parent else "None"
        print(f"{key}: {summary} | Assignee: {assignee} | Epic: {epic}")
else:
    print(response.text)
