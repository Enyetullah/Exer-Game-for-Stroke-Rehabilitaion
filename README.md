# Exer-Game for Stroke Rehabilitation (Webcam ExerGame)

A Python-based **rehabilitation exergame** that uses a webcam + **MediaPipe hand tracking** to control an on-screen “cup” and **catch a moving ball**. The game supports multiple movement patterns (horizontal / vertical / diagonal), adjustable difficulty (1–5), automatic level up/down, and **session logging** so progress can be measured across sessions. It also includes an optional **personalized ML model** (RandomForest) that can predict a likely target “zone” and influence random target spawning.

> **Disclaimer:** This is a research/educational prototype and **not a medical device**. It does not replace clinical advice or supervised therapy.

---

## Table of Contents

* [Features](#features)
* [Project Structure](#project-structure)
* [Requirements](#requirements)
* [Installation](#installation)
* [Run the Game](#run-the-game)
* [How to Play](#how-to-play)
* [Game Modes](#game-modes)
* [Difficulty / Progression](#difficulty--progression)
* [Data Logging](#data-logging)
* [Healthy Benchmarks](#healthy-benchmarks)
* [Optional: Personalized ML Model](#optional-personalized-ml-model)
* [Troubleshooting](#troubleshooting)
* [Safety Notes](#safety-notes)
* [Credits](#credits)
* [Author](#author)
* [License](#license)

---

## Features

* Real-time **webcam hand tracking** (MediaPipe + OpenCV)
* Interactive gameplay + menus (PyGame)
* **6 modes**

  * **Random Games:** Horizontal / Vertical / Diagonal (supports ML-based zone prediction if a model exists)
  * **Workout Games (Fixed):** Horizontal / Vertical / Diagonal (structured practice)
* **Difficulty levels (1–5)** with **automatic adjustment**
* **Session logging**

  * CSV logs per session
  * Rolling “recent sessions” history JSON per mode
* **Healthy benchmark** support for comparisons

---

## Project Structure

```txt
Exer-Game-for-Stroke-Rehabilitaion/
  data/
    benchmark/
      healthy_benchmarks.json
      averageScript.py
    <user_name>/
      session_<game_type>_<timestamp>.csv
      <game_type>_history.json
      model_<game_type>.pkl               (optional)
      scaler_<game_type>.pkl              (optional)
      columns_<game_type>.txt             (optional)
  models/
    model.py                              # trains personalized models from CSV logs
  src/
    game/
      main.py                             # entry point
      login.py
      horizontalRandomGame.py
      verticalRandomgame.py
      diagonalRandomGame.py
      horizontalFixedGame.py
      verticalFixedGame.py
      diagonalFixedGame.py
    images/
    music/
```

---

## Requirements

* **Python 3.9+** recommended
* A working **webcam**
* Packages used by this project:

  * `pygame`
  * `opencv-python`
  * `mediapipe`
  * `numpy`
  * `pandas`
  * `scikit-learn`
  * `joblib`

> If MediaPipe fails to install on your Python version, try Python **3.10 or 3.11**.

---

## Installation

### 1) Clone the repo

```bash
git clone https://github.com/Enyetullah/Exer-Game-for-Stroke-Rehabilitaion.git
cd Exer-Game-for-Stroke-Rehabilitaion
```

### 2) Create and activate a virtual environment (recommended)

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3) Install dependencies

> This repo may not include a `requirements.txt`. If you do not have one, install manually:

```bash
pip install pygame opencv-python mediapipe numpy pandas scikit-learn joblib
```

---

## Run the Game

From the repo root:

```bash
python src/game/main.py
```

### What happens when you start

1. A **login screen** appears → enter a username.
2. The game creates a folder:

   * `data/<your_username>/`
3. Pick a **mode** and **difficulty**.
4. Play a session — logs are saved automatically.

---

## How to Play

1. Stand/sit in front of your webcam in good lighting.
2. Keep your hand visible to the camera.
3. Your tracked hand controls the in-game “cup” (the catching cursor).
4. Catch the moving ball by placing the cup where the ball travels.

### Controls

* **ESC**: Exit current mode / return to menu
* **ENTER** (after session ends): start next session / continue

> Primary control is through **hand position** detected by the webcam.

---

## Game Modes

### Random Games (varied practice + optional ML)

* **Horizontal Random Game**
* **Vertical Random Game**
* **Diagonal Random Game**

Random modes can optionally use a trained model (if present) to predict a likely “zone” and bias new spawns.

### Workout Games (Fixed / structured practice)

* **Horizontal Workout**
* **Vertical Workout**
* **Diagonal Workout**

Fixed modes follow structured patterns and are useful for consistent practice and benchmarking.

---

## Difficulty / Progression

The game supports **difficulty levels 1–5**. In general:

* Higher levels increase challenge (e.g., speed, timing, or target behavior).
* The system can **level up** after strong performance and **level down** after weak performance.

(Exact tuning depends on the current mode implementation.)

---

## Data Logging

All logs are saved under:

```txt
data/<user_name>/
```

### Session CSV logs

Each session produces a CSV such as:

```txt
session_<game_type>_<timestamp>.csv
```

Typical fields may include:

* `timestamp`
* `trial`
* `ball_x`, `ball_y`
* `cup_x`, `cup_y`
* `zone` (example: left/center/right or top/middle/bottom)
* `success` (1 = catch, 0 = miss)
* `difficulty`
* `game_type`

### Rolling history JSON

Each mode also maintains a rolling session history file, for example:

```txt
horizontal_random_history.json
vertical_fixed_history.json
```

These history files store recent session summaries and can be used for quick progress review.

---

## Healthy Benchmarks

Some fixed modes can compare your results to a stored healthy-user benchmark:

```txt
data/benchmark/healthy_benchmarks.json
```

### Recompute benchmarks (optional)

If you collected tester data and want to generate average benchmarks, run:

```bash
python data/benchmark/averageScript.py
```

Inside `averageScript.py`, update the `testers = [...]` list to match the tester folder names under `data/`.

---

## Optional: Personalized ML Model

The project includes a training script:

```txt
models/model.py
```

It trains:

* a **RandomForestClassifier**
* a **StandardScaler**
  using your session CSV logs.

### Train a model

From the repo root:

```bash
python models/model.py --user "YourUserName" --game-type horizontal_random
```

Valid `--game-type` values used by the project:

* `horizontal_random`
* `vertical_random`
* `diagonal_random`
* `horizontal_fixed`
* `vertical_fixed`
* `diagonal_fixed`

### Model output files

Saved under:

```txt
data/<user_name>/
  model_<game_type>.pkl
  scaler_<game_type>.pkl
  columns_<game_type>.txt
```

### How it is used

If a model exists for your username + game type, **Random** modes may use it to predict a likely zone and bias where the next ball spawns.

> Tip: Collect multiple sessions first (more data → better personalization).

---

## Troubleshooting

### Webcam not detected / black screen

* Close other apps using the webcam (Zoom/Teams/Discord, browser tabs, etc.).
* If needed, change camera index in code:

  * `cv2.VideoCapture(0)` → `cv2.VideoCapture(1)`

### MediaPipe install issues

Upgrade pip:

```bash
pip install --upgrade pip
```

If problems persist, use Python **3.10 or 3.11**.

### Asset path errors (important!)

If you see `FileNotFoundError` for images/music, your code may contain **hard-coded absolute paths** (example: `D:/TruScholars Project/...`).

**Best fix:** change asset loading to **relative paths** using `pathlib`:

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]  # points to src/
IMAGES = BASE_DIR / "images"
MUSIC  = BASE_DIR / "music"

background = pygame.image.load(str(IMAGES / "background.png"))
cup_image  = pygame.image.load(str(IMAGES / "cup.png"))

pygame.mixer.music.load(str(MUSIC / "the-return-of-the-8-bit-era-301292.mp3"))
catch_sound = pygame.mixer.Sound(str(MUSIC / "mixkit-game-ball-tap-2073.wav"))
```

After this change, the project becomes portable across machines.

---

## Safety Notes

This project is intended for **research and educational use** only.

* Start with **low difficulty** and short sessions.
* Use good lighting and keep the camera stable.
* Stop if you feel pain, dizziness, or excessive fatigue.
* Consult a clinician before using any unsupervised rehabilitation software.

---

## Credits

Built with:

* **PyGame** (UI + game loop)
* **OpenCV** (camera capture)
* **MediaPipe** (hand tracking / landmarks)
* **scikit-learn** (optional personalization model)

---

## Author

**Enyetullah Rahimullah (ER)**

---

## Demonstration Link

https://youtu.be/OFtb3gmztT4
