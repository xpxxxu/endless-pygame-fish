# 🐟 Musical Fish - 24/7 Aquarium Live Stream

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0%2B-green.svg)](https://www.pygame.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.20%2B-orange.svg)](https://numpy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An optimized, procedural Python visualizer and generative music generator built for 24/7 continuous streaming (YouTube Live, Twitch, Kick). 

Features a smooth dynamic fish animation, generative pentatonic bell sounds, custom water gradient background, and memory/CPU zero-leak architecture.

---

## 🌟 Key Features

- **Generative Audio System:** Algorithmic pentatonic ambient sound generation synthesized via NumPy with smooth exponential fade-outs.
- **Zero Memory-Leak Architecture:** Pre-cached dynamic rotational angles and pre-synthesized audio buffers to ensure 0% memory accumulation over days of uptime.
- **High Performance Graphics:** Hardware-friendly Pygame surface operations optimized for sustained High-Definition (1080p @ 60 FPS) video encoding.
- **Interactive Gameplay Elements:** Autonomous fish AI feeding loop with dynamic size scaling and bubble particles.

---

## ⚡ Performance Optimizations (24/7 Ready)

| Component | Standard Implementation | Musical Fish Optimization |
| :--- | :--- | :--- |
| **Rotation Engine** | Continuous `pygame.transform.rotate()` every frame | **Cached 360° Angle Lookup Matrix** |
| **Audio Synthesis** | Dynamic `numpy` array generation per event | **8-Tone Synthesized Sound Memory Cache** |
| **Text Rendering** | Frame-by-Frame `Font.render()` call | **State-Triggered Event Re-rendering** |

---

## 🛠️ Quick Setup

### Prerequisites
- Python 3.8 or higher installed on your system.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/xpxxxu/endless-pygame-fish.git

**Install dependencies:**
  ```bash
pip install -r requirements.txt

