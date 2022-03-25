"""
REST API Jira - get Development - Get transition statuses ids
"""

import sys
import json
import base64
import os
import re
import getpass
import datetime
import csv
import requests
from requests.auth import HTTPBasicAuth
#from urllib2 import Request, urlopen, URLError
try:
    from jira import JIRA
    import unittest
except Exception as e:
    print(e)

# Jira settings
JIRA_URL="https://cadalys.atlassian.net"
JIRA_API="/rest/api/2/"
JIRA_USERNAME = "rose.peterson@cadalys.com"
#JIRA_PASSWORD=getpass.getpass(prompt='Password: ', stream=None) 
JIRA_TOKEN="HRsrB1KCDQD5m7hvmVcw6F33" # https://id.atlassian.com/manage/api-tokens
JIRA_PROJECT_KEY = "CCIQ"
JIRA_ISSUE_TYPE = "Story"

# Auth via token 
url = JIRA_URL  + JIRA_API
print(url)
auth = HTTPBasicAuth(JIRA_USERNAME, JIRA_TOKEN)
headers = {
    "Accept": "application/json"
}

# get issuetypes
def jira_rest_issuetypes(data):
    try:
        response = requests.get(url + data, auth=auth)
    except Exception as e:
        print("Failed to connect to ", url, "Error: ",  e)
        return 1
    #print(response.content)
    json_data= json.loads(response.text)
    #print(json_data)
    for item in json_data:
        print("=====================> ",item['id'], item['name'])
    
#get transition inf for issues
def get_transitions(data):
    tr_url = JIRA_URL 
    options={"server": tr_url}
    try:
        jira_instance = JIRA(options, basic_auth=(JIRA_USERNAME, JIRA_TOKEN))
    except Exception as e:
        print("Failed to connect to ", url, "Error: ",  e)
        return 1

    issue = jira_instance.issue('CCIQ-1241')
    print("Issue transitions ====>",issue)
    transitions = jira_instance.transitions(issue)
    [(t['id'], t['name']) for t in transitions] 
    #print([(t['id'], t['name']) for t in transitions])

    #worklfow transitios
    response = requests.get(url + 'workflow/search?expand=transitions', auth=auth)
    json_data= json.loads(response.content)
    #print("ALL transitions ====>", json_data, "\n<======= All transitions\n")

    workflowName='CCIQ SDLC WORKFLOW'
    tr_url=url + 'workflow/search?expand=transitions&workflowName=' + workflowName
    response = requests.get(tr_url, auth=auth)
    json_data= json.loads(response.content)
    #print("Workflow ", workflowName, " transitions ====>", json_data, "<======= end Workflow transition\n")
    for transition in json_data['values']:
        #print("\n - Transition -> ", transition['transitions'][1]['name'])
        for tran in transition['transitions']:
            print("\n - tran -> ", tran)

    return 0

    #https://cadalys.atlassian.net/rest/api/3/workflow/transitions/{transitionId}/properties?workflowName={workflowName}' \
    #https://cadalys.atlassian.net/rest/api/3/workflow

# Get issues Development 
def jira_jql():
    url = JIRA_URL 
    print(url)
    options={"server": url}
    jira_instance = JIRA(options, basic_auth=(JIRA_USERNAME, JIRA_TOKEN))
    print("Issues with moore than 5 PRs")
    projs = jira_instance.projects()
    #for p in projs:
    #    print(p)
    allfields=jira_instance.fields()
    nameMap = {field['name']:field['id'] for field in allfields}

    #JQL - custom field Development=11500
    query = """
    PROJECT = "CCIQ"
    AND status not in ("Not Needed", "Needs Info", Back-Burner, Closed, Resolved, Closed., Resolved., Cancelled, Done, Released) 
    AND issuetype = Story
    AND development[commits].all > 5
    ORDER BY lastViewed DESC
    """
    my_jql = jira_instance.search_issues(query) # get key and id
    for issue in my_jql:
        print (issue.key)
        issue_url=url + issue.key
        meta = jira_instance.editmeta(issue)
        issue = jira_instance.issue(issue)
        dev_com=getattr(issue.fields, nameMap['Development'])
        print("Development: ",dev_com)

   # PEND get start commit end commit dates =>


jira_rest_issuetypes('project/CCIQ/statuses')
get_transitions('project/CCIQ/statuses')
#jira_jql()

exit(0)
