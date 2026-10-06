# Proof of concept

import requests
from bs4 import BeautifulSoup

def fetch_page():
    url = "https://www.unitedutilities.com/help-and-support/your-water-supply/your-reservoirs/reservoir-levels/"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    print(r.status_code)
    print("Regional Total" in r.text)

def parse_percent("60.2%"):
    pass

def parse_date("9th August 2026"):
    pass

def parse_table(html):
    pass

