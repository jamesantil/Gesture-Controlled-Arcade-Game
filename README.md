Gesture-Controlled Arcade Game 🎮✋

A Summer of Code project exploring computer vision and hand-tracking, building up from OpenCV fundamentals to a custom real-time gesture recognition system — the foundation for a gesture-controlled arcade game.

Project Overview

This repo documents a 4-week progression through computer vision and gesture recognition using OpenCV and MediaPipe, moving from basic image processing to a working hand-gesture classifier that can be mapped to game controls.


📁 Repository Structure

Gesture-Controlled-Arcade-Game/
├── Week1/    # OpenCV fundamentals
├── Week2/    # MediaPipe hand tracking + applied mini-projects
├── Week3/    # Custom gesture classification (finger-counting)
├── Week4/    # Robust gesture recognition (handedness + distance-based)


Week 1 — OpenCV Fundamentals

Set up the development environment (Python, VS Code) and worked through core OpenCV concepts: reading/writing images, rescaling, color spaces and channels, blurring, edge detection, contour detection, masking, bitwise operations, histograms, image transformations, and basic face detection with Haar cascades.

Week 2 — Introduction to MediaPipe

Learned MediaPipe's hand-tracking pipeline and built two applied projects on top of it:


HandTrackingModule.py — a reusable hand detector class wrapping MediaPipe Hands, returning landmark positions for downstream use.
handTrackingMin.py — minimal hand landmark detection with FPS counter.
VolumeHandControl.py — controls system volume based on the distance between thumb and index finger, using pycaw.
bicepcurl.py — a rep counter using MediaPipe Pose, calculating elbow joint angles to detect curl stages and count repetitions.


Week 3 — Gesture Classification (v1)

Built a first version of finger-counting-based gesture classification on top of the hand tracking module:


week3_gestures.py — detects finger up/down states and classifies basic gestures: FIST, OPEN PALM, POINTING, PEACE, THUMBS UP.


Week 4 — Gesture Classification (v2, robust)

Refactored gesture detection into a standalone, testable module with improvements:


gestures.py — finger-state detection that accounts for handedness (left/right), plus distance-based gesture detection (e.g. OK sign via thumb-index pinch) normalized by hand scale so it works at different distances from the camera.
HandTrackingModule.py — extended with findHandLabel() to detect left/right hand.
test_gestures.py — integration test combining hand tracking + gesture classification in a live webcam feed.



🛠️ Tech Stack


Python 3.11
OpenCV — image processing & video capture
MediaPipe — hand & pose landmark detection
NumPy — numerical computation (angles, interpolation)
pycaw — Windows audio control



🚀 Running the Project

Each week's scripts can be run independently:

bashpip install opencv-python mediapipe numpy pycaw
python Week4/test_gestures.py

Press d to quit any webcam window.


🎯 Next Steps


Map recognized gestures to in-game controls
Build the arcade game logic
Integrate gesture input as the primary controller for gameplay



📚 Resources Used


MediaPipe Hands paper (arXiv)
MediaPipe Hands docs
Murtaza's Workshop — Hand Tracking & Gesture Volume Control tutorials
Nicholas Renotte — AI Pose & Hand Estimation tutorials
freeCodeCamp — OpenCV full course
