"""
Read a list of NTEE codes and descriptions into a CSV
"""
import pandas as pd
from bs4 import BeautifulSoup
import requests

ntee_url = 'https://urbaninstitute.github.io/nccs-legacy/ntee/ntee.html'
table_class = 'table table-hover table-sm'

def read_table_rows(table) -> list:
    table_contents = []
    table_body = table.find('tbody')
    for tr in table_body.find_all('tr'):
        row_data = []
        row_data.append(tr.find('th').text.strip())
        for data in tr.find_all('td'):
            row_data.append(data.text.strip())
        if len(row_data) != 3:
            raise ValueError(f"The table row {tr.find('th').text.strip()}does not have 3 values.")
        table_contents.append(row_data)
    return table_contents

def scrape_ntee_codes():
    res = requests.get(ntee_url, timeout=120)
    soup = BeautifulSoup(res.content, features="lxml")
    table = soup.find(class_=table_class)
    if not table: 
        raise ValueError(f"The NTEE page does not contain htmls element of the class '{table_class}'.")
    table_tag = table.find_all('thead')[0]
    column_names = [subtag.text.strip() for subtag in table_tag.find_all('th')]
    table_contents = read_table_rows(table)
    df = pd.DataFrame(table_contents, columns=column_names)
    df.to_csv('data/ntee.csv', index=False)

scrape_ntee_codes()