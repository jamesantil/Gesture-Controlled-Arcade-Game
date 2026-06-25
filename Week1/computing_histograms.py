import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

img = cv.imread('C:/Users/james/Desktop/CV/Photos/website.jpg')
cv.imshow('natural', img)

blank = np.zeros(img.shape[:2], dtype='uint8')

circle=cv.circle(blank, (img.shape[1]//2, img.shape[0]//2), 100, 255, -1)



# gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# cv.imshow('gray',gray)

mask=cv.bitwise_and(img, img,mask=circle)

cv.imshow('masked', mask)

##grascale histogram
# gray_hist=cv.calcHist([gray], [0], mask , [256], [0,256] )

# plt.figure()
# plt.title('Grayscale histogram')
# plt.xlabel('Bins')
# plt.ylabel('# of pixels')
# plt.plot(gray_hist)
# plt.show()


##colour histogram
plt.figure()
plt.title('Color histogram')
plt.xlabel('Bins')
plt.ylabel('# of pixels')
colors=('b','g','r')
for i,col in enumerate(colors):
    hist= cv.calcHist([img], [i], None, [256], [0,256])
    plt.plot(hist,color=col)
    plt.xlim([0,256])
    
plt.show()


cv.waitKey(0)