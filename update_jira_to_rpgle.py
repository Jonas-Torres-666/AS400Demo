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

def generate_rpgle_tasks(email, token, domain):
    url = f"https://{domain}/rest/api/3/search/jql"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}
    query = {
        "jql": "assignee = currentUser() ORDER BY created DESC",
        "maxResults": 5,
        "fields": "summary,key"
    }
    
    response = requests.request("GET", url, headers=headers, params=query, auth=auth)
    
    if response.status_code == 200:
        issues = response.json().get("issues", [])
        
        rpgle_content = "**free\n"
        rpgle_content += "// Generated Jira Tasks for AS/400 Demo\n\n"
        rpgle_content += "dcl-proc printJiraTasks export;\n"
        
        if not issues:
            rpgle_content += "  snd-msg 'No Jira tasks found.';\n"
        else:
            for issue in issues:
                key = issue.get("key")
                summary = issue.get("fields", {}).get("summary", "No Summary").replace("'", "''")
                rpgle_content += f"  snd-msg '{key}: {summary}';\n"
        
        rpgle_content += "end-proc;\n"
        
        with open("qrpglesrc/jiratasks.rpgle", "w") as f:
            f.write(rpgle_content)
        print("Successfully generated qrpglesrc/jiratasks.rpgle")
    else:
        print(f"Error fetching Jira tasks: {response.status_code}")

if __name__ == "__main__":
    load_env()
    EMAIL = os.environ.get("JIRA_EMAIL")
    TOKEN = os.environ.get("JIRA_TOKEN")
    DOMAIN = os.environ.get("JIRA_DOMAIN", "demoia.atlassian.net")
    
    if EMAIL and TOKEN:
        generate_rpgle_tasks(EMAIL, TOKEN, DOMAIN)
    else:
        print("Missing credentials in .env")
