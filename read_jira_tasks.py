import requests
from requests.auth import HTTPBasicAuth
import json
import sys
import os

def load_env():
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value

def get_jira_tasks(email, token, domain="demoia.atlassian.net"):
    url = f"https://{domain}/rest/api/3/search/jql"
    
    auth = HTTPBasicAuth(email, token)
    
    headers = {
        "Accept": "application/json"
    }
    
    query = {
        "jql": "assignee = currentUser() ORDER BY created DESC",
        "maxResults": 50,
        "fields": "summary,status,key,issuetype,parent"
    }
    
    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query,
        auth=auth
    )
    
    if response.status_code == 200:
        data = response.json()
        issues = data.get("issues", [])
        if not issues:
            print("No tasks found.")
            return
            
        print(f"{'Key':<12} | {'Type':<10} | {'Summary':<40} | {'Status':<12} | {'Epic'}")
        print("-" * 100)
        for issue in issues:
            fields = issue.get("fields", {})
            key = issue.get("key")
            issuetype = fields.get("issuetype", {}).get("name", "Unknown")
            summary = fields.get("summary", "No Summary")
            status = fields.get("status", {}).get("name", "Unknown")
            
            parent = fields.get("parent", {})
            epic = parent.get("fields", {}).get("summary", "None") if parent else "None"
            epic_key = parent.get("key", "") if parent else ""
            epic_display = f"{epic_key}: {epic}" if epic_key else "None"

            summary = (summary[:37] + "..") if len(summary) > 37 else summary
            epic_display = (epic_display[:27] + "..") if len(epic_display) > 27 else epic_display
            
            print(f"{key:<12} | {issuetype:<10} | {summary:<40} | {status:<12} | {epic_display}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    load_env()
    EMAIL = os.environ.get("JIRA_EMAIL")
    TOKEN = os.environ.get("JIRA_TOKEN")
    DOMAIN = os.environ.get("JIRA_DOMAIN", "demoia.atlassian.net")
    
    if len(sys.argv) > 2:
        EMAIL = sys.argv[1]
        TOKEN = sys.argv[2]
        
    if not EMAIL or not TOKEN:
        print("Usage: python read_jira_tasks.py [EMAIL] [TOKEN]")
        print("Or set JIRA_EMAIL and JIRA_TOKEN in .env or environment.")
        sys.exit(1)
        
    get_jira_tasks(EMAIL, TOKEN, DOMAIN)
