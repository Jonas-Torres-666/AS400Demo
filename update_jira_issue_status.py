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

def get_transitions(issue_key, email, token, domain):
    url = f"https://{domain}/rest/api/3/issue/{issue_key}/transitions"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers, auth=auth)
    return response.json().get('transitions', []) if response.status_code == 200 else []

def update_issue_status(issue_key, email, token, domain, status_name="Done"):
    transitions = get_transitions(issue_key, email, token, domain)
    transition_id = None
    
    # Try to find a transition that matches "Done" or "Finalizado" or similar
    # In Spanish, it's often "Finalizado" or "Hecho" or "Listo"
    target_names = ["Done", "Finalizado", "Hecho", "Completed", "Listo"]
    
    for t in transitions:
        if any(name.lower() in t['name'].lower() for name in target_names):
            transition_id = t['id']
            status_found = t['name']
            break
    
    if not transition_id and transitions:
        # Fallback: just show available ones if no match found
        print(f"Could not find a 'Done' transition for {issue_key}. Available: {[t['name'] for t in transitions]}")
        return False

    url = f"https://{domain}/rest/api/3/issue/{issue_key}/transitions"
    auth = HTTPBasicAuth(email, token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = json.dumps({"transition": {"id": transition_id}})
    
    response = requests.request("POST", url, data=payload, headers=headers, auth=auth)
    
    if response.status_code == 204:
        print(f"Successfully updated {issue_key} to '{status_found}'")
        return True
    else:
        print(f"Failed to update {issue_key}: {response.status_code}")
        print(response.text)
        return False

if __name__ == "__main__":
    load_env()
    EMAIL = os.environ.get("JIRA_EMAIL")
    TOKEN = os.environ.get("JIRA_TOKEN")
    DOMAIN = os.environ.get("JIRA_DOMAIN", "demoia.atlassian.net")
    
    if not EMAIL or not TOKEN:
        print("Missing credentials.")
        sys.exit(1)
        
    for key in ["SCRUM-1", "SCRUM-2"]:
        update_issue_status(key, EMAIL, TOKEN, DOMAIN)
