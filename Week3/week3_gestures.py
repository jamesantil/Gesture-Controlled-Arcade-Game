import cv2 as cv
import time
import HandTrackingModule as htm

cap = cv.VideoCapture(0)

pTime = 0
cTime = 0

detector = htm.handDetector(detectionCon=0.7, maxHands=1)


def fingersUp(lmlist):
    """Returns [thumb, index, middle, ring, pinky], 1 = up, 0 = down."""
    fingers = []
    tips = [4, 8, 12, 16, 20]

    # thumb - bends sideways, compare x (assumes mirrored frame, right hand)
    fingers.append(1 if lmlist[4][1] > lmlist[3][1] else 0)

    # other 4 fingers - compare y, tip above pip joint = up
    for tip in tips[1:]:
        fingers.append(1 if lmlist[tip][2] < lmlist[tip - 2][2] else 0)

    return fingers


def classifyGesture(fingers):
    if fingers == [0, 0, 0, 0, 0]:
        return "FIST"
    if fingers == [1, 1, 1, 1, 1]:
        return "OPEN PALM"
    if fingers == [0, 1, 0, 0, 0]:
        return "POINTING"
    if fingers == [0, 1, 1, 0, 0]:
        return "PEACE"
    if fingers == [1, 0, 0, 0, 0]:
        return "THUMBS UP"
    return "UNKNOWN"


while True:
    success, img = cap.read()
    img = cv.flip(img, 1)  # mirror, feels natural

    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)

    if len(lmlist) != 0:
        fingers = fingersUp(lmlist)
        gesture = classifyGesture(fingers)
        print(fingers, gesture)

        cv.putText(img, gesture, (20, 100), cv.FONT_HERSHEY_SIMPLEX,
                   1.2, (0, 255, 0), 2)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)

    cv.imshow('Image', img)
    if cv.waitKey(1) & 0xFF == ord('d'):
        break
