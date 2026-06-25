import math


def distance(lmlist, p1, p2):
    """Euclidean pixel distance between two landmark indices."""
    x1, y1 = lmlist[p1][1], lmlist[p1][2]
    x2, y2 = lmlist[p2][1], lmlist[p2][2]
    return math.hypot(x2 - x1, y2 - y1)


def handScale(lmlist):
    """Wrist to middle-knuckle distance, used to normalize other distances
    so gestures work the same up close or far from the camera."""
    ref = distance(lmlist, 0, 9)
    return ref if ref != 0 else 1


def fingersUp(lmlist, handLabel="Right"):
    """Returns [thumb, index, middle, ring, pinky], 1 = up, 0 = down."""
    fingers = []

    # thumb bends sideways - direction depends on handedness
    if handLabel == "Right":
        fingers.append(1 if lmlist[4][1] > lmlist[3][1] else 0)
    else:
        fingers.append(1 if lmlist[4][1] < lmlist[3][1] else 0)

    # other 4 fingers - tip above pip joint (smaller y) = up
    for tip in [8, 12, 16, 20]:
        fingers.append(1 if lmlist[tip][2] < lmlist[tip - 2][2] else 0)

    return fingers


def classify(lmlist, handLabel="Right"):
    """Main entry point. Give it a landmark list, get back a gesture name."""
    if not lmlist or len(lmlist) < 21:
        return "NONE"

    fingers = fingersUp(lmlist, handLabel)
    scale = handScale(lmlist)

    # distance-based gestures first - more specific than finger counts
    pinchDist = distance(lmlist, 4, 8) / scale
    if pinchDist < 0.3 and fingers[2] and fingers[3] and fingers[4]:
        return "OK"

    # finger-count gestures
    if fingers == [0, 0, 0, 0, 0]:
        return "FIST"
    if fingers == [1, 1, 1, 1, 1]:
        return "OPEN_PALM"
    if fingers == [0, 1, 0, 0, 0]:
        return "POINT"
    if fingers == [0, 1, 1, 0, 0]:
        return "PEACE"
    if fingers == [1, 0, 0, 0, 0]:
        return "THUMB"

    return "UNKNOWN"
