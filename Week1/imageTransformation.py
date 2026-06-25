import cv2 as cv
import numpy as np
img = cv.imread('C:/Users/james/Desktop/CV/Photos/website.jpg')
cv.imshow('panda mera bhai', img)

##Translation

def translation(img, x, y):     ## x and y are the pixels you want to shift your image with
    transMat = np.float32([[1,0,x], [0,1,y]])
    dimensions = (img.shape[1], img.shape[0])
    return cv.warpAffine(img , transMat , dimensions)
    
## negative x value means shfting to left
## negative y value means shifting to up

# translate = translation(img , 100, 100)
# cv.imshow('translated image' , translate )

##Rotation

def rotate(img, angle, rotPoint=None):
    (height, width) = img.shape[:2]
    
    if rotPoint is None:
        rotPoint = (width//2, height//2)
    rotMat = cv.getRotationMatrix2D(rotPoint , angle, 1.0) ##here 1.0 represents that image should remain 1x, not resizing it now, can do btw
    dimensions =(width,height)
    
    return cv.warpAffine(img, rotMat , dimensions)


# rotated= rotate(img , 45) ## to do clockwise, give negative values
# cv.imshow('rorated image ' , rotated)

##resizing
# resizedd= cv.resize(img, (500,500), interpolaion=cv.INTER_CUBIC)
# cv.imshow('resized', resizedd)

##Flipping
# flip= cv.flip(img,-1) ##0 flip vertical, -1 flip both vertically and horizontally, 1 flip horizontally
# cv.imshow('Flip', flip)

##Cropping

cropped=img[200:300 , 100:400]
cv.imshow('cropped',cropped)
cv.waitKey(0)