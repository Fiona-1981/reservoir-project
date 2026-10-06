# Reservoir Project

A small Python project that scrapes reservoir levels from the
[United Utilities reservoir levels page](https://www.unitedutilities.com/help-and-support/your-water-supply/your-reservoirs/reservoir-levels/),
with the aim of eventually presenting the data through a front end.

Reservoir levels aren't available from the Environment Agency APIs, as they're
published by the individual water companies, so this project gets them by
scraping the web page instead.

## Status

Early proof of concept. So far it can:

- fetch the United Utilities reservoir levels page
- parse percentage strings such as `"51.9%"` into numbers

Still to do: parsing dates and the table of reservoir levels.

## Setup

Requires Python 3.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python3 scrape_uu.py
```

## Running the tests

```bash
python3 -m pytest -v
```

## Built with

- [Requests](https://requests.readthedocs.io/) for fetching the page
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for parsing the HTML
- [pytest](https://docs.pytest.org/) for testing
