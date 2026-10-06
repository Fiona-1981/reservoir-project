# Proof of concept

import requests
from bs4 import BeautifulSoup


def fetch_page():
    url = "https://www.unitedutilities.com/help-and-support/your-water-supply/your-reservoirs/reservoir-levels/"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    print(r.status_code)
    print("Regional Total" in r.text)


def parse_date(text):
    pass


def parse_percent(text):
    percent = float(text.rstrip("%"))
    return percent



def parse_table(html):
    pass


if __name__ == "__main__":
    print(f"Parsed percent: {parse_percent("51.9%")}")
    print(f"Parsed percent: {parse_percent("-3.2%")}")