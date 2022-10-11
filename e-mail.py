#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import json
import os
import sys
import urllib.parse
import argparse
from rich import print
from rich import table
from rich.console import Console
from rich.table import Table

import pandas as pd
import requests

API_URL = 'https://api.dehashed.com/search?query='
API_EMAIL = '<removed>'
API_TOKEN = '<removed>'



if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='e-mail.py')
    parser.add_argument('--domain', help='search for domain', required=True)
    args = parser.parse_args()
    DOMAIN = args.domain



    # GET CONTACTS
    results = []
    try:
        r = requests.get(API_URL + DOMAIN, auth=(API_EMAIL, API_TOKEN), headers={'accept': 'application/json'})
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("ERROR")
        print(e, file=sys.stderr)
    except requests.exceptions.RequestException as e:
        print(e, file=sys.stderr)

    print(API_URL + DOMAIN)
    contacts = r.json()
    print(contacts)

    ## Loop through CONTACTS
    if contacts['entries'] is not None:
        for contact in contacts['entries']:
            try:
                r = requests.get(API_URL + contact['email'], auth=(API_EMAIL, API_TOKEN), headers={'accept': 'application/json'})
                r.raise_for_status()
                print(API_URL + contact['email'])
                secret = r.json()
                if secret['entries'] is not None:
                    for result in secret['entries']:
                        results.append(result)
                else:
                    print("nothing found for: " + contact['email'])
            except requests.exceptions.HTTPError as e:
                print("ERROR")
                print(e, file=sys.stderr)
            except requests.exceptions.RequestException as e:
                print(e, file=sys.stderr)


    table = pd.DataFrame.from_dict(results)
    table.to_csv('result.csv', index=False, header=True)

    ## Create Table Output
    with open('result.csv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        table = Table(
            title="Passwords",
            show_lines=True,
            title_style="white",
            header_style="bright_yellow",
            )
        for row in reader:
            table.add_row(row['email'], row['password'], row['hashed_password'])



    console = Console()
    console.print(table)
