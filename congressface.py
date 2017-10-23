import requests
import json
import time
from datetime import datetime
import numpy as np
from bs4 import BeautifulSoup

BASE_URL = "https://www.congress.gov/members"
HEADERS = { "User-Agent": "Mozilla/5.0" }

def get_attr(item, selector, attr):
  result = item.select(selector)
  out = ""
  if (result):
    out = result[0][attr]
  return out

def get_cell(item, string):
  result = item.find("strong", string=string)
  if result:
    sibling = result.find_next_sibling("span")
    if sibling:
      return sibling.getText()
  return ""

def get_text(item, selector):
  result = item.select(selector)
  if (result):
    return result[0].getText()
  return ""

def parse_list_item(item):
  return {
    "image": get_attr(item, "div.member-image img", "src"),
    "name": get_text(item, ".result-heading"),
    "state": get_cell(item, "State:"),
    "party": get_cell(item, "Party:"),
    "served": get_cell(item, "Served:")
  }

def scrape(page=1):
  r = requests.get(BASE_URL, headers=HEADERS, params={
    "pageSize": 250,
    "page": page
  })
  soup = BeautifulSoup(r.text, 'html.parser')
  items = soup.select("ol.basic-search-results-lists > li.compact")

  return {
    "results": [parse_list_item(item) for item in items],
    "done": not (not soup.select(".next.off"))
  }

def write_json(filename, data):
  with open(filename, 'w') as outjson:
    json.dump(data, outjson)

def collect_congress():
  page = 1
  data = []
  collect = True

  while collect:
    print('collecting page {page}...'.format(page=page))
    result = scrape(page)
    data.extend(result["results"])
    collect = not result["done"]
    page += 1
    time.sleep(1)

  write_json("data/congress.json", {
    "data": data,
    "date": datetime.now().replace(microsecond=0).isoformat()
  })

if __name__ == '__main__':
  collect_congress()