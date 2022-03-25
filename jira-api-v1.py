"""
REST API Jira - 
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
    import csv
except Exception as e:
    print("Error:",e)

# Jira settings
JIRA_URL="https://summusappgroup.atlassian.net"
JIRA_API="/rest/api/2/"
JIRA_USERNAME = "rosegpeterson@gmail.com"
#JIRA_PASSWORD=getpass.getpass(prompt='Password: ', stream=None) 
JIRA_TOKEN="HRsrB1KCDQD5m7hvmVcw6F33" # https://id.atlassian.com/manage/api-tokens
JIRA_ID="CCIQ"

#####  CAREIQ
if JIRA_ID == "CCIQ":
    JIRA_PROJECT_KEY = "CCIQ"
    JIRA_PROJECT = "Cadalys - CareIQ"
    JIRA_SPRINT = "Sprint 10 - GSD"
    JIRA_SPRINT_KEY = "Sprint10"
    SPRINT_START_DATE="2021-09-01"
    SPRINT_END_DATE="2021-09-15"

#####  CSM
if JIRA_ID == "CSM":
    JIRA_PROJECT_KEY = "CADITSM"
    JIRA_PROJECT = "Cadalys - Service Management"
    JIRA_SPRINT = "Sprint 25 - Seattle"
    JIRA_SPRINT_KEY = "Sprint25"
    SPRINT_START_DATE="2021-08-24"
    SPRINT_END_DATE="2021-09-07"

######  CONCIERGE
if JIRA_ID == "CONCIERGE":
    JIRA_PROJECT_KEY = "CADALYSCNG"
    JIRA_PROJECT = "Cadalys - Concierge"
    JIRA_SPRINT = "Sprint 12 - Rome"
    JIRA_SPRINT_KEY = "Sprint12"
    SPRINT_START_DATE="2021-08-31"
    SPRINT_END_DATE="2021-09-14"

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
    
def get_issues_sprint(sprint_name):
    #active_sprints = jira_instance.sprints(board_id=142, state='open')
    #print("Active sprint issues:  ", len(active_sprints))
    #for sprint in active_sprints:
    #    print(sprint)
    #search_issue= 'project="Cadalys - CareIQ"'
    search_issue= 'project="' + JIRA_PROJECT + '"' + ' AND sprint="' + JIRA_SPRINT + '"'
    issues_in_sprint = jira_instance.search_issues(search_issue + ' and issuetype not in subTaskIssueTypes() ORDER BY key', maxResults=MAX_RESULTS, expand='changelog' )
    print("\nNumber of issues in sprint: ", len(issues_in_sprint))
    return issues_in_sprint

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
    #https://summusappgroup.atlassian.net/rest/api/3/workflow/transitions/{transitionId}/properties?workflowName={workflowName}' \
    #https://summusappgroup.atlassian.net/rest/api/3/workflow

def get_projects():
    url = JIRA_URL
    print(url)
    options={"server": url}
    jira_instance = JIRA(options, basic_auth=(JIRA_USERNAME, JIRA_TOKEN))
    projs = jira_instance.projects()
    for p in projs:
        print(p)


# Get issues Development 
def jira_jql():
    url = JIRA_URL 
    print(url)
    options={"server": url}
    jira_instance = JIRA(options, basic_auth=(JIRA_USERNAME, JIRA_TOKEN))
    print("Issues with moore than 5 PRs")
    projs = jira_instance.projects()
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

# Get issues subtask
def get_subtasks(issue_key):
    subtask_issue=[]
    search_subtasks= 'project="' + JIRA_PROJECT + '" and type = Sub-task and parent=' + issue_key
    issues = jira_instance.search_issues(search_subtasks)
    for issue in issues:
        print("Parent %s of subtask %s assignee %s status %s Sprint %s" % (issue.fields.parent, issue.key, issue.fields.assignee, issue.fields.status, JIRA_SPRINT))
        issue_list = ["%s,%s,%s,%s,%s,%s,%s,%s" % (JIRA_PROJECT_KEY,issue.fields.issuetype.name,issue.fields.parent, issue.key, issue.fields.status, issue.fields.assignee, issue.fields.created,JIRA_SPRINT)]
        subtask_issue.append(issue_list)
    return subtask_issue

def get_issues_info(issues_in_sprint):
    commitment = 0
    list_stories=[]
    list_subtasks=[]
    title_stories=["'Project','Sprint','Type','key','points','current_status','last assignee','Date','From','To','Author','Assignee_change'"]
    title_stasks=["'Project','Sprint','Type','Parent','Key','current_status','assignee','Date'"]
    list_stories.append(title_stories)
    for issue in issues_in_sprint:
        issue_type=issue.fields.issuetype.name
        issue_key=issue.key
        issue_status=issue.fields.status
        if ((issue_type == "Story" or issue_type == "Bug" or issue_type == "Defect") and issue_status != 'Not Needed'):
            issue_points=issue.fields.customfield_10004
            commitment += issue_points if issue_points is not None else 0
            #print(issue_type, issue_key, issue_points, issue.fields.status, issue.fields.assignee, issue.fields.summary)
            print(f"Number of Changelog entries found: {issue.changelog.total}") # number of changelog entries 
            for history in issue.changelog.histories:
                history_id = history.id
                for item in history.items:
                    if item.field == 'assignee':
                        assignee_change=item.toString
                    if item.field == 'status':
                        value_to = item.toString.lower()
                        value_from = item.fromString.lower()
                        author=history.author.displayName
                        if value_from == 'in dev'and history.created <= SPRINT_END_DATE and history.created >= SPRINT_START_DATE and author != 'Automation for Jira':
                            try:
                                print(JIRA_PROJECT_KEY,issue_type, issue_key, issue_points, issue.fields.status, issue.fields.assignee, history.created, item.fromString, item.toString, author, assignee_change, JIRA_SPRINT)
                                list_story= ["%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (JIRA_PROJECT_KEY,issue_type, issue_key, issue_points, issue.fields.status, issue.fields.assignee, history.created, item.fromString, item.toString, author, assignee_change, JIRA_SPRINT)]
                                list_stories.append(list_story)
                                print()
                            except Exception as e:
                                print(value_to)
            subtasks=get_subtasks(issue_key)
            list_subtasks.extend(subtasks)
    print("\nALL Stories : ", len(list_stories))
    print("\nALL subtasks : ", len(list_subtasks))
    print("\nTotal commited points: ", commitment)
    #save to file
    FILESTORY = JIRA_PROJECT_KEY + '-' + JIRA_SPRINT_KEY + '-Stories.csv'
    FILESTASK = JIRA_PROJECT_KEY + '-' + JIRA_SPRINT_KEY + '-SubTasks.csv'
    with open(FILESTORY, 'w') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL,delimiter=',')
        writer.writerows(list_stories)
    with open(FILESTASK, 'w') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL,delimiter=',')
        writer.writerows(list_subtasks)


# **** MAIN
#jira_rest_issuetypes('project/CCIQ/statuses')
#get_transitions('project/CCIQ/statuses')
#jira_jql()
#get_projects()

MAX_RESULTS=500
url = JIRA_URL 
print(url)
issues_in_sprint='None'
options={"server": url}
jira_instance = JIRA(options, basic_auth=(JIRA_USERNAME, JIRA_TOKEN))

issues_in_sprint=get_issues_sprint('sprint1')
get_issues_info(issues_in_sprint)
exit(0)
