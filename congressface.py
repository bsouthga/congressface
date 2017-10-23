import requests
import json
import time
import os
import cv2
from datetime import datetime
import numpy as np
from bs4 import BeautifulSoup

BASE_URL = "https://www.congress.gov"
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
  r = requests.get(BASE_URL + "/members", headers=HEADERS, params={
  "pageSize": 250,
  "page": page
  })
  soup = BeautifulSoup(r.text, "html.parser")
  items = soup.select("ol.basic-search-results-lists > li.compact")

  return {
  "results": [parse_list_item(item) for item in items],
  "continue": (not soup.select(".next.off"))
  }

def write_json(filename, data):
  with open(filename, "w") as outjson:
  json.dump(data, outjson)

def collect_congress():
  page = 1
  data = []
  collect = True

  while collect:
  print("collecting page {page}...".format(page=page))
  result = scrape(page)
  data.extend(result["results"])
  collect = result["continue"]
  page += 1
  time.sleep(1)

  write_json("data/congress.json", {
  "data": data,
  "date": datetime.now().replace(microsecond=0).isoformat()
  })

def save_image(url):
  filename = url.split("/")[-1]
  filepath = "images/" + filename

  if os.path.exists(filepath):
  return None

  r = requests.get(BASE_URL + url)

  if r.status_code == 200:
    with open(filepath, "wb") as f:
      f.write(r.content)

def collect_images():
  data_filepath = "data/congress.json"

  if not os.path.exists(data_filepath):
  print("no data file, run collect_congress() first")
  return None

  with open(data_filepath) as data_file:
  data = json.load(data_file)
  members = data["data"]
  for member in members:
    if member["image"] != "":
    print(
      "retrieving image for {name}...".format(
      name=member["name"]
      )
    )
    save_image(member["image"])

def crop_and_center(image):
  facedata = "cvdata/haarcascade_frontalface_alt.xml"
  cascade = cv2.CascadeClassifier(facedata)

  img = cv2.imread("images/" + image)

  minisize = (img.shape[1],img.shape[0])
  miniframe = cv2.resize(img, minisize)

  faces = cascade.detectMultiScale(miniframe)

  for f in faces:
    x, y, w, h = [ v for v in f ]
    cv2.rectangle(img, (x,y), (x+w,y+h), (255,255,255))
    sub_face = img[y:y+h, x:x+w]
    res = cv2.resize(sub_face, (200, 200), interpolation = cv2.INTER_LINEAR)
    return res

  return None


def average_face(filename, images):


if __name__ == "__main__":
  # collect_congress()
  # collect_images()
  facecrop("111_rp_az_5_mitchell_harry_200.jpg")
