# Script to pull protein sequences from UniProt
# UniProt (https://www.uniprot.org) is the world's leading resource for protein sequence info

import requests
import re
from requests.adapters import HTTPAdapter, Retry
from datetime import date

KEYWORDS = ["tau"]
UNIPROT_ENDPOINT = 'https://rest.uniprot.org/uniprotkb/search'
FIELDS = "id,accession,protein_name,sequence,organism_name,length" # https://www.uniprot.org/help/return_fields
RAW_FILE_PATH = "data/raw/sequences.tsv"

# create query for UniProt API
def generate_query(keywords):
    query = "reviewed:true AND " + 'AND'.join(f"keyword:{keyword}" for keyword in keywords)
    return query

# function to get the next link if there are more pages
def get_next_link(headers):
    re_next_link = re.compile(r'<(.+)>; rel="next"')
    if "Link" in headers:
        print(re_next_link)
        match = re_next_link.match(headers["Link"])
        if match:
            return match.group(1)

# function to pull a batch of sequences from Uniprot
def get_batch(batch_url, params):
    page = 1
    while batch_url:
        try:
            if page == 1:
                response = requests.get(batch_url, params=params, timeout=30)
            else:
                response = requests.get(batch_url, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Request failed on page {page}: {e}")
            break
        total = response.headers["x-total-results"]
        yield response, total
        batch_url = get_next_link(response.headers)
        print(batch_url)
        page += 1

if __name__ == "__main__":
    # generate params
    params = {
        "query": generate_query(KEYWORDS),
        "format": "json",
        "fields": FIELDS,
        "size": 500
    }

    # load results into file
    progress = 0
    with open('data/raw/sequences.json', 'w') as f:
        for batch, total in get_batch(UNIPROT_ENDPOINT, params):
            lines = batch.text.splitlines()
            if not progress:
                print(lines[0], file=f)
            for line in lines[1:]:
                print(line, file=f)
            progress += len(lines[1:])
            print(f'{progress} / {total}')