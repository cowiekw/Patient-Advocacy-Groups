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


ntee_codes = ['B01', 'E01', 'E30Z', 'E86', 'E70', 'F01', 'G01', 'G012', 'G20', 'G46Z', 'G50', 'G80', 'H02', 'H12', 'H50', 'H200','S41']

def prepare_api_request()-> str:
    organization = input('Organization: ')
    # state = input('State: ')
    params = {'organization': organization, 'state':None, 'ntee': None}
    api_url = construct_url(params)
    return api_url

def call_propublica_api(api_url:str) -> dict:
    res = re.get(api_url)
    print("Response Status:", res.status_code)
    data = res.json()
    print(f"Raw results: {data['total_results']}")
    pretty = json.dumps(data, indent=4) 
    return data

def filter_by_ntee_code(response_data:dict)-> list:
    filtered_organizations = [
        o for o in response_data["organizations"] if o['ntee_code'] in ntee_codes
    ]
    for o in filtered_organizations:
        print(f"{o['name']}, (ntee:{o['ntee_code']}), {o['ein']}")
    print(f"Filtered results: {len(filtered_organizations)}")
    print(type(filtered_organizations))
    return filtered_organizations

def main():
    api_url = prepare_api_request()
    data = call_propublica_api(api_url)
    organizations = filter_by_ntee_code(data)

if __name__=="__main__":
    main()

   