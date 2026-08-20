# endless-pygame-fish
# Endless Procedural Fish Simulation (24/7 Stream)

A continuous, endless simulation built entirely in Python using Pygame. The fish swims, eats, and grows endlessly in a procedurally generated environment.

## 🚀 Features
* **No Image Assets:** All visuals (fish, food, bubbles, background) are drawn dynamically using pure geometry and vector math.
* **Procedural Audio:** Uses `numpy` to generate harmonic, pentatonic-scale ambient tones continuously in the background. No pre-recorded audio files are used!
* **Optimized for 24/7:** Designed with a stable loop to maintain memory and CPU efficiency for continuous live streaming.

## 🛠️ Requirements & How to Run

1. Make sure you have Python installed, then install the required libraries:
   ```bash
   pip install pygame numpy
## 🎥 The 24/7 Live Stream Architecture

Running a continuous stream requires more than just launching the game. Here is a detailed breakdown of how I set up the 24/7 streaming environment using **OBS Studio** and **Python**:

### 1. Game Execution & Crash Handling
Running a Python script indefinitely can sometimes lead to unexpected crashes. To prevent the stream from freezing, I use a simple auto-restart script.
* **Auto-Restart (Batch Script):** Instead of running `python fish.py` directly, I use a `.bat` (or `.sh`) script with an infinite loop. If the Pygame window crashes or closes, the script instantly relaunches it.
* **Resource Management:** The Pygame `Clock.tick()` is carefully set to cap the framerate (e.g., 30 or 60 FPS) to prevent the `while` loop from consuming 100% of the CPU.

### 2. OBS Studio Setup
The game logic is separated from the streaming software to maintain performance. 
* **Video Capture:** I use the **"Window Capture"** source in OBS pointing to the Pygame window. *Note: The window must remain open in the background (not minimized), or OBS might stop rendering it.*
* **Audio Capture:** To avoid streaming my system sounds (like notifications), I use OBS's **"Application Audio Capture"** specifically targeted at the Python process, isolating the procedural `numpy` sounds.
* **Stream Settings:** Since it's a 2D geometric game, I use a lower video bitrate (around 2500 - 3000 kbps). This keeps the stream smooth, reduces CPU encoding load, and saves internet bandwidth for a 24/7 upload.

### 3. OS & Hardware Optimization
To ensure the stream doesn't get interrupted by the operating system:
* **Power Settings:** Sleep mode, screen timeouts, and hard drive sleep features are completely disabled. 
* **Updates:** Automatic OS updates are paused so the PC doesn't force a restart in the middle of the night.
