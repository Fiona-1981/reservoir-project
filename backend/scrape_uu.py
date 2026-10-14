import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from models import Reservoir, Week

# The value columns after the date, in the order UU's table shows them
EXPECTED_COLUMNS = ["Actual stock", "Change since last week", "Average year", "Last year"]


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


def cell_text(cell):
    # strip=True also copes with cells that wrap their value in a stray <p>
    return cell.get_text(strip=True)


def parse_table(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if table is None:
        raise ValueError("No table found on the reservoir levels page")

    thead = table.find("thead")
    header = [cell_text(th) for th in thead.find_all("th")] if thead else []
    if header[1:] != EXPECTED_COLUMNS:
        raise ValueError(
            f"Unexpected table header: expected a date followed by "
            f"{EXPECTED_COLUMNS}, got {header}"
        )
    try:
        week_date = parse_date(header[0])
    except ValueError as err:
        raise ValueError(f"Could not read a date from the table header: {header[0]!r}") from err

    tbody = table.find("tbody")
    rows = tbody.find_all("tr") if tbody else []
    if not rows:
        raise ValueError("Reservoir levels table has no rows")

    reservoirs = []
    for row in rows:
        name_cell = row.find("th")
        if name_cell is None:
            raise ValueError(f"Table row has no reservoir name: {cell_text(row)!r}")
        name = cell_text(name_cell)
        values = [cell_text(td) for td in row.find_all("td")]
        if len(values) != len(EXPECTED_COLUMNS):
            raise ValueError(
                f"Expected {len(EXPECTED_COLUMNS)} values for {name!r}, "
                f"got {len(values)}: {values}"
            )
        actual_stock, change, average_year, last_year = (parse_percent(v) for v in values)
        reservoirs.append(Reservoir(
            name=name,
            actual_stock=actual_stock,
            change_since_last_week=change,
            average_year=average_year,
            last_year=last_year,
        ))

    return Week(date=week_date, reservoirs=reservoirs)



if __name__ == "__main__":
    print(f"Parsed percent: {parse_percent("51.9%")}")
    print(f"Parsed percent: {parse_percent("-3.2%")}")
    print(f"Parsed date: {parse_date("27th September 2026")}")
    print(parse_table)
