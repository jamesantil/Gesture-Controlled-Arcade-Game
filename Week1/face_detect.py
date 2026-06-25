import cv2 as cv
import numpy as np

img = cv.imread('C:/Users/james/Desktop/CV/Photos/anadearmas.webp')
cv.imshow('natural', img)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('gray person', gray)


haar_cascade = cv.CascadeClassifier('haar_face.xml')
faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)

print(f'Number of faced found = {len(faces_rect)}')

for(x,y,w,h) in faces_rect:
    cv.rectangle(img, (x,y), (x+w, y+h), (0,255,0), thickness=2)
    
cv.imshow('detected faces', img)

cv.waitKey(0)