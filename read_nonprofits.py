"""
Search nonprofits by making an API request to ProPublica.Search by name, state, or NTEE code. 
"""
from datetime import datetime
import json
import urllib
import pandas as pd
import requests as re

STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
        "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
        "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
        "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
        "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "ZZ"]


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
    res = re.get(api_url, timeout=120)
    if not res.status_code== 200:
        raise LookupError('Nonprofit search failed.')
    data = res.json()
    print(json.dumps(data, indent=4))
    return data


def load_to_df(data:dict) -> pd.DataFrame:
    columns = ['name', 'ein', 'ntee_code', 'city', 'state', 'have_filings',
               'have_pdfs']
    org_dicts = []
    for o in data["organizations"]:
        org_data = {col: o[col] for col in columns}
        org_dicts.append(org_data)
    return pd.DataFrame.from_dict(org_dicts)


def export_to_csv(df:pd.DataFrame, ntee_code:str):
    output_name = f'out/nonprofits_{ntee_code}.csv'
    df.to_csv(output_name, index=False)


def search_nonprofit_by_ntee():
    ntee_code = int(input('NTEE CODE (number 1-11): '))
    print(type(ntee_code), ntee_code)
    params = {'organization': None, 'state': None, 'ntee': ntee_code}
    api_url = construct_url(params)
    data = fetch_data(api_url)
    df = load_to_df(data)
    export_to_csv(df, ntee_code)

    # Check request and results
    print(f"API url: {api_url}")
    print(df.name)


if __name__=="__main__":
    search_nonprofit_by_ntee()
    print(f'Completed at {datetime.now()}')
