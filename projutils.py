"""
Utils
"""

import sys
import json
import base64
import os
import re
try:
    import yaml
    import unittest
    import csv
except Exception as e:
    print("Error:",e)

YMLFILE="prodconf.yml"

def read_yaml_file():
    ymldata=''
    jiratoken=''
    with open(YMLFILE, 'r') as f:
        try:
            ymldata=yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print("Failed opening ", YMLFILE, exc)
    return ymldata


#Calls
confdata=read_yaml_file()
authinf=confdata['jirasec']
#print(authinf['JIRA_USERNAME'])
for k in authinf:
   foo=k.split(",")
   print("=>",foo)
