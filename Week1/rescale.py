import cv2 as cv


def rescaleFrame(frame, scale):  ##can use for any image, video, live video
    width = int(frame.shape[1]*scale)
    height = int(frame.shape[0]*scale)
    
    dimensions = (width, height)
    
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)


def changeRes(width, height):   ##Live video
    capture.set(3,width)
    capture.set(4,height)
    ## maybe there's 10 for brightness

capture=cv.VideoCapture('C:/Users/james/Desktop/CPI badh rahi hai.mp4')

while True:
    isTrue , frame = capture.read()
    
    resized_frame=rescaleFrame(frame, 0.25)
    
    cv.imshow('orginal video', frame)
    cv.imshow('resize one',resized_frame)
    
    if cv.waitKey(30) & 0xFF==ord('d'):
        break

capture.release()
cv.destroyAllWindows()  