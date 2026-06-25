import cv2 as cv
import numpy as np
import time
import math
from pycaw.pycaw import AudioUtilities
import HandTrackingModule as htm
###############################
wCam, hCam = 640, 480
###############################

device = AudioUtilities.GetSpeakers()
volume = device.EndpointVolume
# print(f"Audio output: {device.FriendlyName}")
# print(f"- Muted: {bool(volume.GetMute())}")
# print(f"- Volume level: {volume.GetMasterVolumeLevel()} dB")
# print(f"- Volume range: {volume.GetVolumeRange()[0]} dB - {volume.GetVolumeRange()[1]} dB")
# volume.SetMasterVolumeLevel(0, None)
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol=0
volBar=400
volPer=0


cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0


detector = htm.handDetector(detectionCon=0.7)




while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) !=0: 
        # print(lmList[4], lmList[8])
        
        x1, y1 =lmList[4][1] , lmList[4][2]
        x2, y2 =lmList[8][1] , lmList[8][2]
        cx, cy =(x1+x2)//2 , (y1+y2)//2
        
        cv.circle(img, (x1,y1), 10, (255,0,255) , cv.FILLED )
        cv.circle(img, (x2,y2), 10, (255,0,255) , cv.FILLED )
        cv.line(img, (x1,y1), (x2, y2), (255,0,255), 3)
        cv.circle(img, (cx,cy), 10, (255,0,255) , cv.FILLED )

        length= math.hypot(x2-x1,y2-y1)
        print(length)
        
        if length<30:
                    cv.circle(img, (cx,cy), 10, (255,0,0) , cv.FILLED )

        
        ##Hand range 30 - 300
        ##Volume Range -65   -   0
        vol = np.interp(length, [50,300], [minVol,maxVol])
        volBar = np.interp(length, [50,300], [400,150])
        volPer = np.interp(length, [50,300], [0,100])
        volume.SetMasterVolumeLevel(vol, None)
        
    cv.rectangle(img, (50,150), (85,400), (0,255,0), 2)
    cv.rectangle(img, (50,int(volBar)), (85,400), (0,255,0), cv.FILLED)
    cv.putText(img, f'{int(volPer)} %', (40,450), cv.FONT_HERSHEY_COMPLEX,1,(0,250,0), 3)
    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime= cTime
    
    cv.putText(img, f'FPS: {int(fps)}', (40, 70), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    
    cv.imshow("Img", img)
    if cv.waitKey(1) & 0xFF==ord('d'):  
        break