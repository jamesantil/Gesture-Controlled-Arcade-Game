"""
Week 6 - Directional Gesture Classifier
-----------------------------------------
Week 3/4's gestures.py could already tell FIST / OPEN_PALM / PEACE / etc.
apart using finger counts, but for Snake I need one more thing: which
*direction* the index finger is pointing (up / down / left / right), not
just "a finger is up".

This module reuses the exact same fingersUp() logic from gestures.py, and
adds an angle-based direction check for the pointing gesture, using the
same atan2 trick shown in the Week 6 reference material, just adapted to
work with the (id, px, py) pixel-coordinate landmark list that my own
HandTrackingModule.findPosition() returns, instead of MediaPipe's raw
normalized landmarks.
"""

import math


def fingersUp(lmlist, handLabel="Right"):
    """Returns [thumb, index, middle, ring, pinky], 1 = up, 0 = down.
    Same logic as Week 3/4's gestures.py."""
    fingers = []

    if handLabel == "Right":
        fingers.append(1 if lmlist[4][1] > lmlist[3][1] else 0)
    else:
        fingers.append(1 if lmlist[4][1] < lmlist[3][1] else 0)

    for tip in [8, 12, 16, 20]:
        fingers.append(1 if lmlist[tip][2] < lmlist[tip - 2][2] else 0)

    return fingers


def pointingAngle(lmlist):
    """Angle (in degrees) of the index finger: vector from the index MCP
    joint (landmark 5, the knuckle) to the index fingertip (landmark 8).

    0 deg   -> pointing right
    90 deg  -> pointing up
    +-180   -> pointing left
    -90 deg -> pointing down

    dy is flipped (mcp.y - tip.y) because pixel y grows downward, so a
    finger pointing "up" on screen actually has a *smaller* y at the tip.
    """
    index_mcp = lmlist[5]
    index_tip = lmlist[8]
    dx = index_tip[1] - index_mcp[1]
    dy = index_mcp[2] - index_tip[2]
    return math.degrees(math.atan2(dy, dx))


def classifyDirectional(lmlist, handLabel="Right"):
    """Main entry point for the game. Turns a landmark list into one of:
    FIST, OPEN PALM, POINT UP, POINT DOWN, POINT LEFT, POINT RIGHT, NONE.
    """
    if not lmlist or len(lmlist) < 21:
        return "NONE"

    fingers = fingersUp(lmlist, handLabel)
    count = sum(fingers)

    # unambiguous regardless of hand angle, so check these first
    if count == 0:
        return "FIST"
    if count == 5:
        return "OPEN PALM"

    # anything else (1-4 fingers up) -> use pointing direction
    angle = pointingAngle(lmlist)
    if -60 <= angle <= 60:
        return "POINT RIGHT"
    elif 60 < angle < 120:
        return "POINT UP"
    elif angle >= 120 or angle <= -120:
        return "POINT LEFT"
    else:
        return "POINT DOWN"
