# Proof of concept

import requests

url = "https://www.unitedutilities.com/help-and-support/your-water-supply/your-reservoirs/reservoir-levels/"
r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
print(r.status_code)
print("Regional Total" in r.text)
