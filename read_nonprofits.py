"""
Search nonprofits by making an API request to ProPublica.
Search by name or NTEE code. 
API Docs: https://projects.propublica.org/nonprofits/api
"""
import requests as re
import json
import sys

def construct_url(params:dict):
    url = 'https://projects.propublica.org/nonprofits/api/v2/search.json?'
    if params.get('organization'):
        url += f"q={params['organization']}"
    if params.get('state'):
        if url[-1] != '?':
            url = url+'&'
        url += f"state%5Bid%5D=={params['state']}"
    if params.get('ntee'):
        if url[-1] != '?':
            url +='&'
        url += f"ntee%5Bid%5D=D=={params['ntee']}"
    return url

organization = input('Organization: ')
state = input('State: ')
params = {'organization': organization, 'state':state, 'ntee': None}
api_url = construct_url(params)
print(f"Request url: {api_url}\n")

res = re.get(api_url)
print("Status: ", res.status_code)
data = res.json()
for o in data["organizations"]:
    print(f"{o['name'], ({o['ntee_code']})")
