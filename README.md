# Gesture Controlled Arcade Game 🎮✋
 
A Snake game you play entirely with **hand gestures** — no keyboard, no mouse — built as part of Seasons of Code (SOC '26).
 
Uses a live webcam feed, MediaPipe hand-landmark detection, a custom gesture classifier, and a Pygame game engine, merged into a single real-time loop.
 
<!-- Optional: add a GIF/screenshot of the game running here -->
<!-- ![demo](assets/demo.gif) -->
 
---
 
## 🎯 Problem Statement
 
Most casual arcade games are built around keyboard/controller input only — there's no natural, touchless way to interact with them. This project explores whether a real-time game can be controlled **entirely through webcam-based hand gesture recognition**, while staying:
- **Responsive** — despite webcam frame rates (18–30fps) being far slower and less consistent than a typical 60fps game loop
- **Reliable** — despite raw gesture detection being noisy frame-to-frame
- **Intuitive** — using a small, unambiguous gesture vocabulary instead of a complex sign language
## 💡 Approach
 
```
Webcam Frame → MediaPipe Hand Landmarks → Gesture Classifier → Stability Filter → direction → Snake moves
```
 
1. **Hand tracking** — [MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker)'s `HandLandmarker` model detects 21 keypoints per hand (wrist, knuckles, fingertips) from each webcam frame.
2. **Gesture classification** (`game_gestures.py`) — two-stage:
   - **Finger counting**: compares each fingertip's position to the joint below it → 0 fingers up = `FIST`, 5 up = `OPEN PALM` (reliable regardless of hand angle).
   - **Pointing direction**: for 1–4 fingers up, the index finger's angle (via `atan2` on the vector from knuckle → fingertip) is bucketed into `POINT UP` / `DOWN` / `LEFT` / `RIGHT`.
3. **Stability filter** — a gesture only takes effect after being detected for **4 consecutive frames** (~0.2s), to ignore the brief "transition" gestures your hand passes through when rotating between directions.
4. **Game engine** (`gesture_snake_game.py`) — a grid-based Snake game built in Pygame. The game logic only ever reads a single `direction` variable — it doesn't care whether that came from an arrow key or a gesture, which is what makes swapping input sources clean.
## 🕹️ Gesture → Action Map
 
| Gesture | Action |
|---|---|
| ✊ Fist | Start game / restart after game over |
| ☝️ Point Up / Down / Left / Right | Move the snake |
| ✋ Open Palm | Pause (point in any direction to resume) |
 
Keyboard controls (arrow keys, `P` pause, `G` grid toggle, `+`/`-` speed, `Q` quit) also work as a backup input path.
 
## ✨ Features
 
- Real-time gesture-controlled movement with a stability filter to prevent flicker
- Persistent high score (saved to `highscore.txt`)
- Adjustable speed, toggleable grid overlay
- Live webcam feedback window showing the currently detected gesture
- Progressive speed-up as the snake eats
## 🛠️ Tech Stack
 
- **Python 3**
- **[MediaPipe](https://ai.google.dev/edge/mediapipe)** — hand landmark detection (`HandLandmarker` Tasks API)
- **OpenCV** — webcam capture & frame processing
- **Pygame** — game engine & rendering
- **NumPy** — angle/vector math (bicep curl tracker module)
## 📁 Project Structure
 
```
.
├── Week 1/            # Python fundamentals
├── Week 2/            # MediaPipe / CV theory
├── Week 3/            # First hand landmark detection scripts
├── Week 4/            # Gesture classification (finger counting)
├── Week 5/            # Keyboard-controlled Snake game
├── Week 6/            # Gesture-controlled Snake game (final project)
│   ├── HandTrackingModule.py    # Wraps MediaPipe HandLandmarker
│   ├── game_gestures.py         # Finger-count + angle-based gesture classifier
│   ├── gesture_snake_game.py    # Main game loop
│   └── hand_landmarker.task     # Pre-trained MediaPipe model
└── README.md
```
 
## 🚀 Getting Started
 
### Prerequisites
```bash
pip install pygame opencv-python mediapipe numpy
```
 
### Run the game
```bash
cd "Week 6"
python gesture_snake_game.py
```
Two windows will open: the Snake game, and a webcam feedback window showing your hand landmarks and the currently detected gesture — useful for confirming your gestures are being read correctly.
 
> **Note on MediaPipe versions:** MediaPipe removed the legacy `mp.solutions` API in pip releases `0.10.30+`. This project uses the current **Tasks API** (`HandLandmarker` + `hand_landmarker.task`) for compatibility with all recent MediaPipe versions.
 
## 📊 Results
 
- Gesture detection runs at ~18–25 fps depending on lighting and hardware.
- Gameplay speed is decoupled from webcam frame rate (via `pygame.time.get_ticks()`), so the game stays smooth and consistent regardless of camera performance.
- The stability filter eliminates the accidental direction-flip issue caused by transient in-between hand poses.
## 🔮 Future Improvements
 
- Migrate the Week 1–4 bicep curl tracker (`mp.solutions.pose`) to the Tasks API (`PoseLandmarker`) for the same version compatibility fix
- Add more gestures (e.g. pinch-to-select for a menu)
- Expand beyond Snake to other gesture-controlled arcade games
## 🙏 Acknowledgements
 
Built as part of **Seasons of Code (SOC '26)**, project ID 40.
Hand tracking built on [Google's MediaPipe](https://ai.google.dev/edge/mediapipe).
