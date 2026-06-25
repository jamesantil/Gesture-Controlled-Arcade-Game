import cv2 as cv
import matplotlib.pyplot as plt

img = cv.imread('C:/Users/james/Desktop/CV/Photos/website.jpg')
cv.imshow('normal', img)


# plt.imshow(img)
# plt.show()

##BGR to GRAYSCALE

# gray = cv.cvtColor(img , cv.COLOR_BGR2GRAY)
# cv.imshow('gray', gray)

# ##BGR to HSV
hsv=cv.cvtColor(img, cv.COLOR_BGR2HSV)
# cv.imshow('hsv', hsv)

# ##BGR ti LAB or L*a*b
lab=cv.cvtColor(img, cv.COLOR_BGR2LAB)
# cv.imshow('Lab', lab)

# ##BGR to RGB
# rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
# cv.imshow('rgb', rgb)
# plt.imshow(rgb)
# plt.show()


##we can change grayscale to bgr, hsv to bgr, lab to bgr but can't directly do grayscale to hsv or things like that cuz see bgr is must between conversions ok

##HSV to BGR
hsv_bgr =cv.cvtColor(hsv,cv.COLOR_HSV2BGR)
cv.imshow('HSV-->BGR', hsv_bgr)

##LAB to BGR
lab_bgr =cv.cvtColor(lab,cv.COLOR_LAB2BGR)
cv.imshow('LAB-->BGR', lab_bgr)

cv.waitKey(0)