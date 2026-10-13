# Reservoir Project

A small project that scrapes reservoir levels from the
[United Utilities reservoir levels page](https://www.unitedutilities.com/help-and-support/your-water-supply/your-reservoirs/reservoir-levels/)
and presents them through a simple web front end.

Reservoir levels aren't available from the Environment Agency APIs, as they're
published by the individual water companies, so this project gets them by
scraping the web page instead.

## Project structure

The project is split into parts that can be worked on independently:

```
backend/    Python scraper that fetches and parses the reservoir levels page
contract/   Sample JSON showing the data shape shared by back end and front end
frontend/   Web page that displays the data as a table and a chart
```

The `contract/sample.json` file defines the agreed data format. The front end
reads it today; the plan is for the back end to produce a file in the same
shape, so the two sides can be developed separately.

## Status

Early proof of concept.

**Back end** can:

- fetch the United Utilities reservoir levels page
- parse percentage strings such as `"51.9%"` into numbers
- parse dates such as `"27th September 2026"`
- read the date from the reservoir levels table

**Front end** can:

- show a table of the latest week's reservoir levels from `contract/sample.json`
- show a line chart of levels over time, one line per reservoir

Still to do:

- parse the full table of reservoir levels in the back end
- publish the scraped data (e.g. to S3, on a schedule) and have the front end
  read it instead of the sample file

## Back end

Requires Python 3.12 or later.

### Setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Usage

```bash
python3 scrape_uu.py
```

### Running the tests

```bash
python3 -m pytest -v
```

The tests use a saved copy of the page in `tests/fixtures/`, so they don't need
a network connection.

## Front end

The page loads its data with `fetch`, so it needs to be served over HTTP rather
than opened directly as a file. From the project root:

```bash
python3 -m http.server
```

Then open <http://localhost:8000/frontend/>.

## Built with

- [Requests](https://requests.readthedocs.io/) for fetching the page
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for parsing the HTML
- [pytest](https://docs.pytest.org/) for testing
- [Chart.js](https://www.chartjs.org/) for the chart
