# Reservoir Project

A small project that scrapes reservoir levels from the
[United Utilities reservoir levels page](https://www.unitedutilities.com/help-and-support/your-water-supply/your-reservoirs/reservoir-levels/)
and presents them through a simple web front end.

Live site: <https://reservoirlevels.dev>

Reservoir levels aren't available from the Environment Agency APIs, as they're
published by the individual water companies, so this project gets them by
scraping the web page instead.

## Project structure

The project is split into parts that can be worked on independently:

```
backend/    Python scraper, data models and AWS Lambda handler
contract/   Sample JSON showing the data shape shared by back end and front end
frontend/   Web page that displays the data as a table and a chart
```

The `contract/sample.json` file defines the agreed data format. The back end
writes its history to S3 in the same shape, and the front end reads it from
there. The tests check the sample file against the back end's models.

## How it fits together

1. Every Thursday at 09:00 UK time, an EventBridge schedule runs the
   `reservoir-levels-scraper` Lambda function in `eu-west-2`.
2. The function scrapes the United Utilities page and saves the week to an S3
   bucket, as `snapshots/<date>.json` and as part of `history.json`.
3. The front end, hosted on Cloudflare Workers, loads `history.json` from the
   bucket and shows it as a table and a chart.

## Status

Working end to end: the back end runs weekly on AWS and the live site shows
the data it collects.

**Back end** can:

- fetch the United Utilities reservoir levels page
- parse the full table of reservoir levels, including the regional total:
  actual stock, change since last week, average year and last year
- fail with a clear error if the table's layout changes
- load and write the contract format using Pydantic models (`models.py`)
- run as an AWS Lambda function that saves each week's levels to S3 and keeps
  a running history (`handler.py`)

**Front end** can:

- load the collected history from S3
- show a table of the latest week's reservoir levels, including the regional
  total
- show a line chart of levels over time, one line per reservoir (the regional
  total is left out of the chart)
- adjust the chart size for phone screens

## Back end

Requires Python 3.12 or later.

### Setup

The virtual environment lives in the project root. From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements-dev.txt
```

`requirements.txt` lists only what the Lambda function needs.
`requirements-dev.txt` adds boto3 and the testing packages for local use.

### Usage

With the virtual environment activated, from the `backend/` folder:

```bash
cd backend
python3 scrape_uu.py
```

This fetches the live page once and prints the latest week as JSON in the
contract format. It needs a network connection.

### Running the tests

From the `backend/` folder:

```bash
python3 -m pytest -v
```

The tests use a saved copy of the page in `tests/fixtures/`, so they don't need
a network connection or AWS. They also check that `contract/sample.json`
matches the Pydantic models.

### Naming

Python code uses snake_case (`actual_stock`) and the JSON contract uses
camelCase (`actualStock`). The models in `models.py` are the one place that
translates between the two.

### Lambda function

`handler.lambda_handler` runs the whole back end once:

1. fetches and parses the live page
2. writes that week to `snapshots/<date>.json`
3. reads `history.json`, adds the week (replacing it if that date is already
   there), and writes `history.json` back

The S3 bucket name comes from the `BUCKET_NAME` environment variable. The
merging logic lives in `merge_week`, which doesn't touch S3, so it can be
tested on its own.

To build the deployment package, with the virtual environment activated:

```bash
backend/build.sh
```

This creates `backend/lambda.zip` for Python 3.14 on arm64, containing the
code and the packages in `requirements.txt`.

When deploying:

- give the function's role `s3:GetObject`, `s3:PutObject` and `s3:ListBucket`
  on the bucket. Without `s3:ListBucket`, S3 reports a missing `history.json`
  as "access denied", and the first run fails instead of starting a new history
- set the timeout to around 30 seconds, as the default of 3 seconds may be too
  short for fetching the page
- choose the Python 3.14 runtime and the arm64 architecture, to match the
  build. Lambda already provides `boto3`, so it isn't in the zip

## Front end

The page loads its data with `fetch`, so it needs to be served over HTTP rather
than opened directly as a file. From the project root:

```bash
python3 -m http.server
```

Then open <http://localhost:8000/frontend/>.

The page loads `history.json` from the S3 bucket, even when running locally.
The bucket's CORS rules allow requests from the live site and from
`http://localhost:8000`, so use that port when testing locally.

### Hosting

The front end is hosted on Cloudflare Workers as a static site, at
<https://reservoirlevels.dev> and
<https://reservoir-levels.fiona-087.workers.dev>. The settings are in
`wrangler.jsonc`:

- `assets.directory` is `./frontend`, so only the front end's files are
  published. The back end, contract and other project files never reach the
  site, and `index.html` is served at the site's root
- `workers_dev` keeps the `workers.dev` address switched on
- `preview_urls` is off, so Cloudflare doesn't publish separate preview
  addresses

To deploy by hand from the project root:

```bash
npx wrangler deploy
```

If the site's address changes or a new domain is added, add it to the S3
bucket's CORS rules too, or the page won't be able to load `history.json`.

## Built with

- [Requests](https://requests.readthedocs.io/) for fetching the page
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for parsing the HTML
- [Pydantic](https://docs.pydantic.dev/) for the data models
- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) for reading and writing S3
- [pytest](https://docs.pytest.org/) for testing
- [Chart.js](https://www.chartjs.org/) for the chart
- [AWS Lambda, S3 and EventBridge](https://aws.amazon.com/) for the back end
- [Cloudflare Workers](https://developers.cloudflare.com/workers/) for hosting the front end
