import cv2 as cv

img = cv.imread('C:/Users/james/Desktop/CV/Photos/website.jpg')  ## this converts the image to pixel matrix and stores it in img variable

cv.imshow('Photoji', img)  ## showing the img, here we passed the matrix of pixel which is stores in img variable

cv.waitKey(0) ## this is to wait infinitly for the user to press any key


##---------below is video reading part-----------------------------------------------------------


# cap= cv.VideoCapture('C:/Users/james/Desktop/CPI badh rahi hai.mp4')

# while True:
#     isTrue, frame = cap.read() ## one one frame comes in frame, reads video frame by frame
    
#     cv.imshow('Video of me', frame) ##shows individual frame one by one after each loop
    
#     if cv.waitKey(1) & 0xFF==ord('d'):  ## wait for this sec and if pressed 'd' then break, 1000==1second, it delays the execution
#         break
    
# cap.release()
# cv.destroyAllWindows()