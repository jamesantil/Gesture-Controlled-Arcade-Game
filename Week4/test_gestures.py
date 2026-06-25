import cv2 as cv
import time
import HandTrackingModule as htm
import gestures

cap = cv.VideoCapture(0)

pTime = 0
cTime = 0

detector = htm.handDetector(detectionCon=0.7, maxHands=1)

while True:
    success, img = cap.read()
    img = cv.flip(img, 1)  # mirror, feels natural

    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)

    gesture = "NONE"
    if len(lmlist) != 0:
        handLabel = detector.findHandLabel()
        gesture = gestures.classify(lmlist, handLabel)

    cv.putText(img, gesture, (20, 100), cv.FONT_HERSHEY_SIMPLEX,
               1.3, (0, 255, 0), 2)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)

    cv.imshow('Gesture Test', img)
    if cv.waitKey(1) & 0xFF == ord('d'):
        break
