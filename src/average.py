import os
import cv2
import json
import numpy as np
from data import prep_data


def average_group(df, groupby):
  df = prep_data()
  key = "-".join(groupby)
  for group, group_df in df.groupby(groupby):
    images = set(list(group_df['image']))
    n = len(images)
    if n > 10:
      print("generating image for group {group} ({n} images)...".format(
        group=group, n=n
      ))
      generate_averages(key + '-' + group + '.png', images)

def generate_averages(filename, images):
  centered = []
  for image in images:
    result = crop_and_center(image)
    if result is not None:
      centered.append(result)

  average = np.average(np.array(centered), axis = 0)
  cv2.imwrite("output/" + filename, average)

def crop_and_center(image):
  facedata = "cvdata/haarcascade_frontalface_alt.xml"
  cascade = cv2.CascadeClassifier(facedata)

  img = cv2.imread("images/" + image, cv2.IMREAD_GRAYSCALE)

  if img is None:
    return None

  minisize = (img.shape[1], img.shape[0])
  miniframe = cv2.resize(img, minisize)

  faces = cascade.detectMultiScale(miniframe)

  for f in faces:
    x, y, w, h = [ v for v in f ]
    cv2.rectangle(img, (x, y), (x + w, y + h), (255,255,255))
    sub_face = img[y:y + h, x:x + w]
    res = cv2.resize(sub_face, (200, 200), interpolation = cv2.INTER_LINEAR)
    return res

  return None