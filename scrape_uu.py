import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def fetch_page():
    url = "https://www.unitedutilities.com/help-and-support/your-water-supply/your-reservoirs/reservoir-levels/"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    return r.text


def parse_date(text):
    # "27th September 2026" -> date(2026, 9, 27)
    without_suffix = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", text.strip())
    return datetime.strptime(without_suffix, "%d %B %Y").date()


def parse_percent(text):
    percent = float(text.rstrip("%"))
    return percent


def parse_table(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find_all("table")[0]
    th = table.find_all("th")[0]
    return parse_date(th.get_text(strip=True))



if __name__ == "__main__":
    print(f"Parsed percent: {parse_percent("51.9%")}")
    print(f"Parsed percent: {parse_percent("-3.2%")}")
    print(f"Parsed date: {parse_date("27th September 2026")}")
    print(parse_table)
