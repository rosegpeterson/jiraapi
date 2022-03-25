curl \
   -D- \
   -X GET \
   -H "Content-Type: application/json" \
   https://cadalys.atlassian.net/rest/api/3/status
   https://cadalys.atlassian.net/rest/api/3/status/search?jql=project=CCIQ&fields=name,id
https://cadalys.atlassian.net/rest/api/3/status?fields=id,name
