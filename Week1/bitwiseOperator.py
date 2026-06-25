import cv2 as cv
import numpy as np

blank=np.zeros((400,400), dtype='uint8')

rectangle=cv.rectangle(blank.copy(), (30,30), (370,370), 255, -1)
circle=cv.circle(blank.copy(), (200,200), 200, 255, -1)

cv.imshow('rectangle', rectangle)
cv.imshow('circle', circle)

##bitwise AND
bitwise_and= cv.bitwise_and(rectangle,circle)
cv.imshow('bitwise and of rec and cir', bitwise_and)

##bitwise OR
bitwise_or=cv.bitwise_or(rectangle,circle)
cv.imshow('bitwise or of rec and cir', bitwise_or)


##bitwise XOR
bitwise_xor=cv.bitwise_xor(rectangle,circle)
cv.imshow('bitwise xor of rec and cir', bitwise_xor)


##bitwise NOT
bitwise_not= cv.bitwise_not(rectangle)
cv.imshow('bitwise not of rec',bitwise_not)

cv.waitKey(0)