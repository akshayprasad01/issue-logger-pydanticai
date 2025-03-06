import os
from jira import JIRA

JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_KEY = os.getenv("JIRA_API_KEY")

def get_jira_client():
    # Connect to Jira
    jira_client = JIRA(server=JIRA_URL, basic_auth=(JIRA_EMAIL, JIRA_API_KEY))
    return jira_client