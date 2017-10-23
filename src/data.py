import os
import json
import sys
import re
import pandas as pd
from dateutil.parser import parse

house_regex = re.compile(r"(?P<house>(?:House:)\s+[\d\-,\s]+)", re.X | re.S)
senate_regex = re.compile(r"(?P<senate>(?:Senate:)\s+[\d\-,\s]+)", re.X | re.S)

#
# extract different year ranges
#
def parse_years(member, current):
  raw = member["served"].strip()
  house = [ m.groupdict() for m in house_regex.finditer(raw) ]
  senate = [ m.groupdict() for m in senate_regex.finditer(raw) ]
  years = { "house": set(), "senate": set() }

  if house:
    string = house[0]["house"].replace("House:", "").strip()
    years["house"].update(parse_years_from_str(string, current))
  if senate:
    string = senate[0]["senate"].replace("Senate:", "").strip()
    years["senate"].update(parse_years_from_str(string, current))

  return years

#
# return set of years contained in string
#
def parse_years_from_str(string, current):
  out = set()
  ranges = string.strip().split(",")
  for year_range in ranges:
    year_range_split = year_range.split("-")
    if len(year_range_split) == 1:
      out.update({ int(year_range_split[0]) })
    else:
      [start, end] = year_range_split
      out.update(set(range(
        int(start),
        current if year_range.endswith("-") else int(end)
      )))
  return out

#
# caveats:
#   - doesn't account for switching party
#
def prep_data():
  data = get_data()
  members = data["data"]
  current_date = parse(data["date"])
  out = []

  for member in members:
    image = member["image"].split('/')[-1]
    if image:
      years = parse_years(member, current_date.year)
      for wing in years:
        for year in years[wing]:
          out.append({
            "year": year,
            "image": image,
            "party": member["party"],
            "wing": wing
          })

  return pd.DataFrame(out)

#
# read data from json
#
def get_data():
  data_filepath = "data/congress.json"

  if not os.path.exists(data_filepath):
    print("no data file, run collect_congress() first")
    sys.exit(1)


  with open(data_filepath) as data_file:
    data = json.load(data_file)
    return data