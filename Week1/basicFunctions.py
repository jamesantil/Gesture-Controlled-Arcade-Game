import cv2 as cv

img = cv.imread('C:/Users/james/Desktop/CV/Photos/website.jpg')
# cv.imshow('panda jiiii', img)

##converting to greyscale
# gray = cv.cvtColor(img , cv.COLOR_BGR2GRAY)
# cv.imshow('gray image of panda', gray)


##blur

# blur =cv.GaussianBlur(img, (13,13), cv.BORDER_DEFAULT)  ##for now just mean that(number,number) should be odd and bigger the number, bigger the blur 
# cv.imshow('blur', blur) 

##Edge Cascade

canny = cv.Canny(img, 125 , 175) ##2 threshhold values
cv.imshow('canny', canny) 

##Dilating the edges

# dilate= cv.dilate(canny, (13,13), iterations=1)
# cv.imshow('dialted', dilate)

# ##Eroding
# erode= cv.erode(dilate, (3,3), iterations=1)
# cv.imshow('eroded', erode)

##dilate and edges are just opposite of each other, if we take same values of eroded and dilated function (i.e. iterations and kernels[those number tuple]) then we will get the same canny image

 
##resize
# resized= cv.resize(img, (500,500)) ## will resize the image with ignoring the aspect ratio
# cv.imshow('resized', resized) ## won't be chopped and see the image will be squished or stretched, just all

# resized= cv.resize(img, (500,500), interpolation=cv.INTER_CUBIC) ##smaller than the size gave then use this
# cv.imshow('resized', resized) 

##cropping
cropped= img[50:200, 200:400]
cv.imshow('cropped', cropped)
cv.waitKey(0)