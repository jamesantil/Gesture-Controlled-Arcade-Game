import cv2 as cv
import numpy as np

img = cv.imread('C:/Users/james/Desktop/CV/Photos/website.jpg')
cv.imshow('natural', img)

gray=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('gray',gray)

##Laplaction
lap= cv.Laplacian(gray, cv.CV_64F)
lap=np.uint8(np.absolute(lap))
cv.imshow('laplatian', lap)

##Sobel
sobelx = cv.Sobel(gray, cv.CV_64F, 1, 0)
sobely = cv.Sobel(gray, cv.CV_64F, 0, 1)
combina_sobel= cv.bitwise_or(sobelx, sobely)

cv.imshow('combined sobel', combina_sobel)


cv.imshow('sobelx', sobelx)
cv.imshow('sobely', sobely)

canny=cv.Canny(gray, 150, 175)
cv.imshow('canny', canny)
cv.waitKey(0)