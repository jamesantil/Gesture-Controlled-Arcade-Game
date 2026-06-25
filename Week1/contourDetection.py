import cv2 as cv
import numpy as np

img=cv.imread('C:/Users/james/Desktop/CV/Photos/website.jpg')

cv.imshow('Panda eating bambooooo',img)

blank=np.zeros(img.shape, dtype='uint8')
cv.imshow('Blank', blank)

gray=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('Panda eating bambooooo',gray)

blur = cv.GaussianBlur(gray, (5,5), cv.BORDER_DEFAULT)
# cv.imshow('blur', blur)

canny=cv.Canny(blur, 25, 50)
cv.imshow('Canny Edges', canny)

# canny=cv.Canny(img, 125, 175)
# cv.imshow('Canny Edges1', canny)

# canny=cv.Canny(img, 200, 300)
# cv.imshow('Canny Edges2', canny)


ret, thresh = cv.threshold(gray , 125, 255, cv.THRESH_BINARY)
cv.imshow('thressssss', thresh)

contours, hierarchies = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE) ## takes in the edges and outputs the two values, give contours and hierarchial representation of the contours ||| can also pass canny to this, canny is recommended instead of passing thresh
print (f'{len(contours)} contour(s) found!') 


cv.drawContours(blank, contours, -1, (0,0,255), thickness=1)
cv.imshow('contours drawn', blank )

cv.waitKey(0)