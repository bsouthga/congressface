import os
import cv2
import json
import numpy as np

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