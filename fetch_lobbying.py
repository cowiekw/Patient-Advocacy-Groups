import os 
import json
from dotenv import load_dotenv
import urllib
import requests as re

load_dotenv()
SENATE_API_KEY = os.getenv('SENATE_API_KEY')
BASE_URL = 'https://lda.senate.gov/api/v1/'


def construct_filings_url() -> str:
    params = {
        'filing_year':'2022',
    }
    param_str = urllib.parse.urlencode(params)
    url = BASE_URL + 'search.json?' + param_str
    return url

def fetch_data(api_url:str) -> dict:
    headers = {
        "Authorization": f"Token {SENATE_API_KEY}",
                "Content-Type": "application/json"
    }
    res = re.get(api_url, headers=headers, timeout=120)
    data = res.json()
    print(json.dumps(data, indent=4))
    return data


fetch_data(BASE_URL)

def parse_filing_response(data):
   # Verify that organization of interest is the Client.
   income=  data['results']['income']
   expenses =  data['results']['expenses']
   lobbying_issue = data['results']['lobbying_activities']['general_issue_code_display']
   lobbying_description = data['results']['lobbying_activities']['descriptoin']
