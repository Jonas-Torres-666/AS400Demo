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

def get_issue_details(issue_key, email, token, domain):
    url = f"https://{domain}/rest/api/3/issue/{issue_key}"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}
    
    response = requests.request("GET", url, headers=headers, auth=auth)
    
    if response.status_code == 200:
        issue = response.json()
        fields = issue.get("fields", {})
        
        print(f"Details for {issue_key}:")
        print("-" * 40)
        print(f"Summary:     {fields.get('summary')}")
        print(f"Status:      {fields.get('status', {}).get('name')}")
        print(f"Priority:    {fields.get('priority', {}).get('name')}")
        print(f"Creator:     {fields.get('creator', {}).get('displayName')}")
        print(f"Created:     {fields.get('created')}")
        
        description = fields.get('description')
        print("\nDescription:")
        if description and isinstance(description, dict) and 'content' in description:
            # Jira ADF (Atlassian Document Format) parsing
            for p in description['content']:
                if p['type'] == 'paragraph':
                    for text_node in p.get('content', []):
                        if text_node['type'] == 'text':
                            print(text_node['text'])
        else:
            print("No description provided.")
    else:
        print(f"Error fetching issue details: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    load_env()
    if len(sys.argv) < 2:
        print("Usage: python get_jira_issue_details.py [ISSUE_KEY]")
        sys.exit(1)
        
    ISSUE_KEY = sys.argv[1]
    EMAIL = os.environ.get("JIRA_EMAIL")
    TOKEN = os.environ.get("JIRA_TOKEN")
    DOMAIN = os.environ.get("JIRA_DOMAIN", "demoia.atlassian.net")
    
    if EMAIL and TOKEN:
        get_issue_details(ISSUE_KEY, EMAIL, TOKEN, DOMAIN)
    else:
        print("Missing credentials in .env")
