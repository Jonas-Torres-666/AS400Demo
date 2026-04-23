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
        "maxResults": 10,
        "fields": "summary,status,key"
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
            
        print(f"{'Key':<12} | {'Summary':<50} | {'Status'}")
        print("-" * 80)
        for issue in issues:
            key = issue.get("key")
            summary = issue.get("fields", {}).get("summary", "No Summary")
            status = issue.get("fields", {}).get("status", {}).get("name", "Unknown")
            summary = (summary[:47] + "..") if len(summary) > 47 else summary
            print(f"{key:<12} | {summary:<50} | {status}")
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
