"""
Search nonprofits by making an API request to ProPublica.
Search by name or NTEE code. 
API Docs: https://projects.propublica.org/nonprofits/api
NTEEs:  https://urbaninstitute.github.io/nccs-legacy/ntee/ntee-history.html#overview
"""
import requests as re
import json
import urllib
import pandas as pd
from datetime import datetime

STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
        "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
        "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
        "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
        "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "ZZ"]

NTEE_SEARCH_CODES = [2, 4,7] 
ADVOCACY_NTEE_CODES = ['B01', 'E01', 'E240', 'E30Z', 'E86', 'E70', 'F01', 'G01', 'G012', 'G20', 'G46Z',
            'G50', 'G80', 'H02', 'H12', 'H50', 'H200','S41']

def construct_url(raw_params:dict) -> str:
    BASE_URL = "https://projects.propublica.org/nonprofits/api/v2/"
    raw_params = {k:v for k,v in raw_params.items() if v is not None}

    params = {}
    for key, value in raw_params.items():
        if key == 'organization':
            key = 'q'
        if key == 'state':
            key = 'state[id]'
            if value not in STATES:
                raise TypeError('Invalid state code')
        if key == 'ntee':
            if value not in range(1, 11):
                raise TypeError('Invalid ntee code')
            key = 'ntee[id]'
        
        params[key] = value
    param_str = urllib.parse.urlencode(params)
    url = BASE_URL + 'search.json?' + param_str
    return url


def fetch_data(api_url:str)-> dict:
    res = re.get(api_url)
    print(res.status_code)
    if not res.status_code== 200:
        raise LookupError('Nonprofit search failed.') 
    data = res.json()
    print(f"Raw results count: {data['total_results']}")
    print(json.dumps(data, indent=4))
    return data

def filter_by_ntee(response_data:dict)-> list:
    columns = ['name', 'ein', 'ntee_code', 'city', 'state', 'have_filings',
               'have_pdfs']
    ntee = response_data['selected_ntee'] or 'x'
    for o in response_data["organizations"]:
        print(f"{o['name']}, (ntee:{o['ntee_code']}), ein: {o['ein']}")

    filtered_organizations = [
        o for o in response_data["organizations"] #  if o['ntee_code'] in ADVOCACY_NTEE_CODES
    ]
    if not filtered_organizations:
        print(f"\nNo matching results founds for ntee {ntee}.")

    org_dicts = []
    for o in filtered_organizations:
        org_data = {field: o[field] for field in columns}
        org_dicts.append(org_data)
    return pd.DataFrame.from_dict(org_dicts)

def export_to_csv(df:pd.DataFrame, ntee:int):
    output_name = f'out/nonprofits_ntee{ntee}.csv'
    df.to_csv(output_name, index=False)

def fetch_nonprofits():
    organization = input('Organization: ')
    # for ntee in range(1, 11):
    ntee = None
    params = {'organization': organization, 'state': 'MD', 'ntee': ntee}
    api_url = construct_url(params)
    print("\nURL: ", api_url)
    data = fetch_data(api_url)
    filtered_df = filter_by_ntee(data)
    filtered_df.to_csv('out/nonprofits.csv', index=False)
    # export_to_csv(filtered_df, 111)


if __name__=="__main__":
    fetch_nonprofits()
    print(f'Completed at {datetime.now()}')

   