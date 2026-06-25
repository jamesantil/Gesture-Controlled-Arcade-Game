import cv2 as cv
import numpy as np

img = cv.imread('C:/Users/james/Desktop/CV/Photos/website.jpg')
cv.imshow('natural', img)

gray= cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('gray',gray)

##simple threshHolding
threshold, thresh = cv.threshold(gray, 150, 255, cv.THRESH_BINARY) ##now any value of pixel intensity below 150 is set to 0 and above is set to 1.. kind off pixel on or off
cv.imshow('simple thresh', thresh)

threshold, thresh_inv = cv.threshold(gray, 150, 255, cv.THRESH_BINARY_INV) ##now any value of pixel intensity below 150 is set to 0 and above is set to 1.. kind off pixel on or off
cv.imshow('simple thresh inverse', thresh_inv)


##Adaptive thresholding
adaptive_thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 3)   ##255 is max value
cv.imshow('Adaptive thresholding', adaptive_thresh)

cv.waitKey(0)