"""
REST API Jira - get Development - Get issues with more than 5 PRS
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
JIRA_URL="https://summusappgroup.atlassian.net"
JIRA_USERNAME = "rosegpeterson@gmail.com"
#JIRA_PASSWORD=getpass.getpass(prompt='Password: ', stream=None) 
JIRA_TOKEN="HRsrB1KCDQD5m7hvmVcw6F33" # https://id.atlassian.com/manage/api-tokens
JIRA_PROJECT_KEY = "RPP"
JIRA_ISSUE_TYPE = "Story"

# Auth via token
def jira_rest_issue(data):
    url = JIRA_URL 
    print(url)
    auth = HTTPBasicAuth(JIRA_USERNAME, JIRA_TOKEN)
    headers = {
     "Accept": "application/json"
    }
    response = requests.get(url + '/rest/api/2/issue/' + data, auth=auth)
    print(response.content)

# Get issues Development 
def jira_rest_dev():
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
    PROJECT = "RPP"
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


jira_rest_dev()
#jira_rest_inf_issue('RPP-963')

exit(0)
