import cv2 as cv


img = cv.imread('C:/Users/james/Desktop/CV/Photos/website.jpg')
cv.imshow('normal', img)

##Gaussian blur don't satisfy all the needs we have

##Averageing
average = cv.blur(img , (3,3))
cv.imshow('average blur', average)

##Gaussian blur, more natural
gauss=cv.GaussianBlur(img, (3,3), 0)
cv.imshow('gauss',gauss)


##Median Blur
median = cv.medianBlur(img, 3) ##openCV assumes that kernel size would be 3,3
cv.imshow('median blur', median)


##Bilateral blurring, retains the edges 
bil= cv.bilateralFilter(img, 5, 15, 15)  ##diameter of pixel neighbourhood, sigmaColor, sigmaSpace
cv.imshow('bilateral', bil)

cv.waitKey(0)