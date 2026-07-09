"""
HandTrackingModule.py (Tasks API version)
--------------------------------------------
UPDATE: MediaPipe removed the old `mp.solutions` API from pip releases
0.10.30 and up (see google-ai-edge/mediapipe#6192, #6200). Since only
those newer versions are available for this Python install, this module
has been rewritten on top of the new MediaPipe **Tasks API**
(`HandLandmarker` + a `hand_landmarker.task` model file) instead of the
old `mp.solutions.hands`.

The public interface is unchanged on purpose, so nothing else in the
project needs to change:
    - handDetector(mode, maxHands, detectionCon, trackCon)
    - .findHands(img, draw=True)      -> img
    - .findPosition(img, handNo=0, draw=True) -> [[id, cx, cy], ...]
    - .findHandLabel(handNo=0)        -> "Left" or "Right"

Requires `hand_landmarker.task` to sit in the same folder as this file.
"""

import cv2 as cv
import mediapipe as mp
import os
import time

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hand_landmarker.task")

# The old mp.solutions.hands.HAND_CONNECTIONS constant is gone too, so the
# standard 21-landmark skeleton connections are hardcoded here for drawing.
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),          # thumb
    (0, 5), (5, 6), (6, 7), (7, 8),          # index
    (5, 9), (9, 10), (10, 11), (11, 12),     # middle
    (9, 13), (13, 14), (14, 15), (15, 16),   # ring
    (13, 17), (17, 18), (18, 19), (19, 20),  # pinky
    (0, 17),                                  # palm base
]


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"hand_landmarker.task not found at {MODEL_PATH}. "
                "Download it and place it in the same folder as this file."
            )

        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=MODEL_PATH),
            running_mode=VisionRunningMode.IMAGE,
            num_hands=self.maxHands,
            min_hand_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon,
        )
        self.landmarker = HandLandmarker.create_from_options(options)
        self.results = None   # holds the most recent detection result

    def findHands(self, img, draw=True):
        rgb_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_img)
        self.results = self.landmarker.detect(mp_image)

        if self.results.hand_landmarks:
            h, w, c = img.shape
            for handLms in self.results.hand_landmarks:
                if draw:
                    # draw the skeleton lines
                    for start_id, end_id in HAND_CONNECTIONS:
                        x1, y1 = int(handLms[start_id].x * w), int(handLms[start_id].y * h)
                        x2, y2 = int(handLms[end_id].x * w), int(handLms[end_id].y * h)
                        cv.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    # draw the joints
                    for lm in handLms:
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        cv.circle(img, (cx, cy), 4, (255, 0, 0), cv.FILLED)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmlist = []
        if self.results and self.results.hand_landmarks:
            if handNo < len(self.results.hand_landmarks):
                myHand = self.results.hand_landmarks[handNo]
                h, w, c = img.shape
                for id, lm in enumerate(myHand):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmlist.append([id, cx, cy])
                    if draw:
                        cv.circle(img, (cx, cy), 7, (255, 0, 0), cv.FILLED)
        return lmlist

    def findHandLabel(self, handNo=0):
        """Returns 'Left' or 'Right'. Same caveat as before: relative to
        the unflipped frame, so it'll read reversed if you cv.flip()."""
        label = "Right"
        if self.results and self.results.handedness:
            if handNo < len(self.results.handedness):
                label = self.results.handedness[handNo][0].category_name
        return label


def main():
    pTime = 0
    cTime = 0
    cap = cv.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmlist = detector.findPosition(img)

        cTime = time.time()
        fps = 1 / (cTime - pTime) if cTime != pTime else 0
        pTime = cTime

        cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)

        cv.imshow('Image', img)
        if cv.waitKey(1) & 0xFF == ord('d'):
            break


if __name__ == "__main__":
    main()
