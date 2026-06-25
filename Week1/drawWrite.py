import cv2 as cv
import numpy as np

blank = np.zeros((500,500,3) , dtype='uint8')  ##dummy image, blank image, dtype is just data type of an image, 3 is for colour channel
# cv.imshow('Blank image', blank)

# img = cv.imread('C:/Users/james/Desktop/CV/Photos/website.jpg')
# cv.imshow('Panda eat bamboo', img)


# blank[:] = 0,255,0 ## ye green ke liye
# cv.imshow('green screen', blank)

# blank[:] = 0,0,255 ## ye red ke liye
# cv.imshow('green screen', blank)

# blank[:] = 255,0,0, ## ye blue ke liye
# cv.imshow('green screen', blank)

##drawing the sqaure
# blank[200:300, 200:300] = 90,200,100 ## selective
# cv.imshow('green screen', blank)

##drawing the rectangle
cv.rectangle(blank, (0,0), (blank.shape[1]//2,blank.shape[0]//3), (1,1,255), thickness=3)  ##updates the blank
# ##can use thickness=cv.FILLED,thickness=-1......shape[1]==width,shape[1]==height
# cv.imshow('rectangle', blank)


##draw circle 

cv.circle(blank, (blank.shape[1]//2, blank.shape[0]//2), 50, (1,20,255), thickness=5)
# cv.imshow('circle', blank)


## draw a line

cv.line(blank, (0,0), (blank.shape[1]//2, blank.shape[0]//2), (0,255,0), thickness=10)
cv.imshow('line', blank)


##write text on an image

cv.putText(blank, 'Hello this is text', (225,225), cv.FONT_HERSHEY_COMPLEX, 1.0, (100, 100,200) , thickness=2)
cv.imshow('text', blank)
cv.waitKey(0)