# Gesture-Controlled Arcade Game 🎮✋

A computer vision project that uses real-time hand-tracking to recognize gestures, with the goal of using them as controller input for an arcade-style game. Built using **OpenCV** and **MediaPipe**.

## Project Overview

The core of this project is a hand-tracking and gesture-recognition pipeline built from scratch on top of MediaPipe's hand landmark detection. It evolved through a few applied prototypes — a hand-gesture volume controller and a pose-based bicep curl counter — before converging on a dedicated gesture classification module that can reliably tell apart gestures like a fist, open palm, peace sign, pointing finger, thumbs up, and an OK sign.

The gesture classifier is handedness-aware (works correctly for both left and right hands) and normalizes distances using the hand's own scale, so detection stays accurate whether the hand is close to or far from the camera. This module is what will ultimately be mapped to in-game actions.

### Key components
- **`HandTrackingModule.py`** — a reusable hand detector class wrapping MediaPipe Hands. Returns hand landmark coordinates and the detected hand label (left/right) for any frame.
- **`gestures.py`** — the gesture classification logic. Computes finger up/down states and key landmark distances (normalized by hand scale) to classify gestures: FIST, OPEN_PALM, POINT, PEACE, THUMB, and OK.
- **`test_gestures.py`** — live webcam demo combining hand tracking and gesture classification, with on-screen gesture labels and FPS display.
- **`VolumeHandControl.py`** — an early applied prototype that maps thumb-index finger distance to system volume control using `pycaw`.
- **`bicepcurl.py`** — an applied prototype using MediaPipe Pose to count bicep curl repetitions by tracking elbow joint angles.
- **`handTrackingMin.py`** — a minimal standalone script for raw hand landmark detection, used during early exploration of the MediaPipe Hands API.

---

## 🛠️ Tech Stack
- **Python 3.11**
- **OpenCV** — image processing & video capture
- **MediaPipe** — hand & pose landmark detection
- **NumPy** — numerical computation (angles, interpolation)
- **pycaw** — Windows audio control

---

## 🚀 Running the Project
```bash
pip install opencv-python mediapipe numpy pycaw
python Week4/test_gestures.py
```
Press **`d`** to quit any webcam window.

---

## 🎯 Next Steps
- Map recognized gestures to in-game controls
- Build the arcade game logic
- Integrate gesture input as the primary controller for gameplay

---

## 📚 Resources Used
- [MediaPipe Hands paper (arXiv)](https://arxiv.org/pdf/2006.10214)
- [MediaPipe Hands docs](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker)
- Murtaza's Workshop — Hand Tracking & Gesture Volume Control tutorials
- Nicholas Renotte — AI Pose & Hand Estimation tutorials
- freeCodeCamp — OpenCV full course
