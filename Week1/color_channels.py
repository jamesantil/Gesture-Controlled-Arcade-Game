import cv2 as cv
import numpy as np

img = cv.imread('C:/Users/james/Desktop/CV/Photos/website.jpg')
cv.imshow('normal', img)

blank=np.zeros(img.shape[:2], dtype='uint8')

b,g,r = cv.split(img)

blue=cv.merge([b,blank,blank])
green=cv.merge([blank,g,blank])
red=cv.merge([blank,blank,r])


cv.imshow('blue',blue)
cv.imshow('green',green)
cv.imshow('red',red)


# cv.imshow('blue',b)
# cv.imshow('green',g)
# cv.imshow('red',r)



# print(img.shape)
# print(b.shape)
# print(g.shape)
# print(r.shape)    ##gives the intensity in grayscale method, white means high concentration of that colour, if dark means that low concentration of that colour


# merged = cv.merge([b,g,r])
# cv.imshow('merged img', merged)




cv.waitKey(0)