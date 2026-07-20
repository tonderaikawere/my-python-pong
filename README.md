# 🏓 My Python Pong

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.x-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-39FF14?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-1.0.0-00E6FF?style=for-the-badge)
[![KawerifyTech](https://img.shields.io/badge/KawerifyTech-kawerifytech.com-00E6FF?style=for-the-badge)](https://kawerifytech.com)

**A stunning, feature-rich Python Pong game with neon visuals, AI opponents, power-ups, and particle effects.**

*Developed by [KawerifyTech](https://kawerifytech.com) · A complete Pygame tutorial project.*

[🎮 Features](#-features) &nbsp;·&nbsp;
[🚀 Quick Start](#-quick-start) &nbsp;·&nbsp;
[📖 Tutorial](#-full-tutorial) &nbsp;·&nbsp;
[🎯 Controls](#-controls) &nbsp;·&nbsp;
[🛠️ Contributing](#-contributing)

</div>

---

## ✨ Features

| Category | Feature |
|---|---|
| 🤖 **AI Opponent** | Three difficulty levels: Easy, Medium, Hard with ball-path prediction |
| 👥 **2-Player Mode** | Local split-keyboard multiplayer |
| ⚡ **Power-Ups** | 5 types — Enlarge, Shrink Opponent, Speed Up, Slow Down, Multi-Ball |
| 🌟 **Neon Visuals** | Dark background, glowing paddles, ball trail, particle bursts |
| 💥 **Particle System** | Up to 300 simultaneous particles on hits and scores |
| 🔊 **Synthesised Audio** | Procedural sound effects via numpy — no audio files needed |
| 📳 **Screen Shake** | Satisfying shake on every point scored |
| 🏆 **Win Screen** | Full match stats + animated winner banner |
| ⏸️ **Pause Menu** | Pause, resume, restart, and navigate during a match |
| 🎨 **State Machine** | Clean splash → menu → difficulty → play → win flow |

---

## 🚀 Quick Start

### Prerequisites

- **Python** 3.8 or higher
- **pip** (bundled with Python)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/tonderaikawere/my-python-pong.git
cd my-python-pong

# 2. (Recommended) Create a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the game!
python main.py
```

> **No audio files needed.** All sounds are synthesised at startup using numpy.

---

## 🎯 Controls

### In-Game

| Action | Player 1 | Player 2 / Menu |
|---|---|---|
| Move Up | `W` | `↑` |
| Move Down | `S` | `↓` |
| Pause | `P` | `P` |
| Restart | `R` | `R` |
| Main Menu | `M` | `M` |
| Toggle Sound | `S` (paused) | — |

### In Menus

| Key | Action |
|---|---|
| `↑` / `↓` | Navigate options |
| `Enter` | Confirm / Select |
| `Escape` | Go back |

---

## 📖 Full Tutorial

This section explains how **My Python Pong** is built — from the game loop to the AI opponent. It's a complete Pygame learning guide.

### Project Structure

```
my-python-pong/
├── main.py         # Entry point — initialise pygame, window, game loop
├── game.py         # State machine & core gameplay logic
├── ball.py         # Ball physics, trail, glow rendering
├── paddle.py       # Paddle movement, power-up states, glow rendering
├── particles.py    # Lightweight particle system
├── audio.py        # Procedural sound synthesis
├── ai.py           # AI controller with ball-path prediction
├── powerup.py      # Power-up types, spawning, and effects
├── ui.py           # All screens: splash, menu, HUD, pause, win
├── constants.py    # Centralised configuration
├── requirements.txt
└── LICENSE
```

---

### Chapter 1 — The Game Loop (`main.py`)

Every Pygame game is built around a **game loop** — a `while True` that repeats every frame:

```python
clock = pygame.time.Clock()

while True:
    dt = clock.tick(60)       # Limit to 60 FPS; dt = ms since last frame

    events = pygame.event.get()   # 1. Gather input events
    game.handle_events(events)    # 2. Process input
    game.update(dt)               # 3. Advance game state
    game.draw()                   # 4. Render to the screen
    pygame.display.flip()         # 5. Present the frame
```

**Why `dt` (delta time)?**
Using milliseconds instead of frame count for movement keeps the game speed consistent regardless of frame rate:

```python
# Bad: tied to FPS
self.x += speed

# Good: frame-rate independent
self.x += speed * (dt / 16.67)   # normalised to 60fps
```

---

### Chapter 2 — The State Machine (`game.py`)

Instead of messy `if showing_menu` checks everywhere, My Python Pong uses a **state machine**:

```
SPLASH → MENU → MODE (difficulty) → PLAYING ⇌ PAUSED → WIN
                                                  ↑           |
                                                  └───────────┘
```

Each state is a simple string constant:

```python
STATE_SPLASH  = "splash"
STATE_MENU    = "menu"
STATE_MODE    = "mode"      # difficulty picker
STATE_PLAYING = "playing"
STATE_PAUSED  = "paused"
STATE_WIN     = "win"
```

The `handle_events`, `update`, and `draw` methods all branch on `self.state`:

```python
def draw(self) -> None:
    if self.state == STATE_MENU:
        self.ui.draw_menu(self.menu_sel)
        return
    if self.state == STATE_PLAYING:
        self._draw_game_world()
    ...
```

This keeps each state's logic completely isolated and easy to extend.

---

### Chapter 3 — Ball Physics (`ball.py`)

#### Basic Motion

The ball moves by adding velocity to position every frame:

```python
self.x += self.vx
self.y += self.vy
```

#### Wall Bounce

When the ball hits the top or bottom, we reflect its Y-velocity:

```python
if self.y <= BALL_SIZE // 2:
    self.y  = BALL_SIZE // 2     # push back inside
    self.vy = abs(self.vy)        # always move downward

if self.y >= HEIGHT - BALL_SIZE // 2:
    self.y  = HEIGHT - BALL_SIZE // 2
    self.vy = -abs(self.vy)       # always move upward
```

#### Speed Increase

After each paddle hit, the ball gradually gets faster:

```python
def speed_up(self) -> None:
    speed = math.hypot(self.vx, self.vy)
    if speed < BALL_MAX_SPEED:
        factor  = (speed + BALL_SPEED_INC) / speed
        self.vx *= factor
        self.vy *= factor
```

#### Glow & Trail

The glowing trail is drawn using **alpha-blended circles** at decreasing opacity:

```python
# Trail
for i, (tx, ty) in enumerate(self.trail):
    frac  = i / len(self.trail)
    alpha = int(200 * frac * 0.7)
    # Draw a transparent circle at (tx, ty)

# Glow layers
for r in range(glow_radius, 0, -3):
    alpha = int(55 * (r / glow_radius) ** 1.8)
    # Draw concentric transparent circles
```

---

### Chapter 4 — Paddle Mechanics (`paddle.py`)

#### Movement

Paddle movement is immediate (no acceleration) to keep the game crisp:

```python
def move_up(self)   -> None: self.vel_y = -PADDLE_SPEED
def move_down(self) -> None: self.vel_y =  PADDLE_SPEED
def stop(self)      -> None: self.vel_y =  0.0
```

#### Spin Mechanic (In `game.py`)

The most important Pong mechanic: **where the ball strikes the paddle changes its angle**:

```python
# rel_y: -1 (top) → 0 (centre) → +1 (bottom)
rel_y   = (ball.y - paddle_center) / (paddle_height / 2)

# Apply spin proportional to contact position
ball.vy = rel_y * abs(ball.vx) * 0.85
```

This gives skilled players control over where they aim the ball.

---

### Chapter 5 — The AI Opponent (`ai.py`)

#### Ball Path Prediction

The AI doesn't just track the ball's current Y — it **predicts** where the ball will be when it arrives at the paddle:

```python
def _predict(self, ball) -> float:
    # Time until ball reaches paddle X
    steps = (paddle_x - ball.x) / ball.vx

    # Estimated Y at arrival
    py = ball.y + ball.vy * steps

    # Simulate wall bounces (fold the value)
    while py < BALL_SIZE or py > HEIGHT - BALL_SIZE:
        if py < BALL_SIZE:
            py = 2 * BALL_SIZE - py
        if py > HEIGHT - BALL_SIZE:
            py = 2 * (HEIGHT - BALL_SIZE) - py

    return py
```

#### Difficulty via Error Injection

Difficulty is a single `accuracy` float (0.0 → 1.0). Lower accuracy adds more random error to the AI's target:

```python
error        = (1 - self.accuracy) * random.uniform(-HEIGHT * 0.38, HEIGHT * 0.38)
self.target_y = predicted_y + error
```

| Level  | `accuracy` | Behaviour |
|--------|-----------|-----------|
| Easy   | `0.30`    | Frequently misses by large margins |
| Medium | `0.65`    | Occasionally misjudges the ball |
| Hard   | `0.95`    | Near-perfect tracking with tiny errors |

---

### Chapter 6 — The Particle System (`particles.py`)

Each `Particle` has position, velocity, lifetime, and size. They fade out and shrink over time:

```python
def update(self) -> None:
    self.x  += self.vx
    self.y  += self.vy
    self.vx *= 0.92          # friction: slow down over time
    self.vy *= 0.92
    self.life -= 1

def draw(self, surf) -> None:
    frac  = self.life / self.max_life   # 1.0 at birth → 0.0 at death
    alpha = int(255 * frac)             # fade out
    size  = int(self.size * frac)       # shrink
    # draw transparent circle
```

The `ParticleSystem` manages a list and culls dead particles:

```python
def emit_burst(self, x, y, color, count=45) -> None:
    for _ in range(count):
        self.particles.append(Particle(x, y, color))

def update(self) -> None:
    self.particles = [p for p in self.particles if p.alive]
    for p in self.particles:
        p.update()
```

---

### Chapter 7 — Procedural Audio (`audio.py`)

All sounds are **mathematically generated** — no audio files required! We build numpy arrays and convert them to pygame Sound objects:

```python
import numpy as np

t    = np.linspace(0, duration, n_samples)     # time axis
data = np.sin(2 * np.pi * freq * t)            # pure sine wave

# Volume envelope: fade in, then fade out
env = np.ones(n_samples)
env[:attack_n]      = np.linspace(0, 1, attack_n)    # attack
env[n - decay_n:]   = np.linspace(1, 0, decay_n)     # decay

data   = (data * env * volume * 32767).astype(np.int16)
stereo = np.column_stack([data, data])          # mono → stereo
sound  = pygame.sndarray.make_sound(stereo)     # pygame Sound
```

Different waveforms give different timbres:

| Waveform | Formula | Sound |
|---|---|---|
| Sine | `sin(2πft)` | Pure, smooth tone |
| Square | `sign(sin(2πft))` | Harsh, buzzy |
| Triangle | `2·|2·(ft - floor(ft + 0.5))| - 1` | Mellow, retro |

---

### Chapter 8 — Power-Ups (`powerup.py`)

Five power-ups spawn at random positions every ~12 seconds:

| Power-Up | Label | Effect | Duration |
|---|---|---|---|
| Enlarge | `BIG` | Your paddle grows 70% | 8 s |
| Shrink Opponent | `SHRINK` | Opponent's paddle shrinks 45% | 8 s |
| Speed Up | `FAST` | Ball velocity × 1.3 | Permanent |
| Slow Down | `SLOW` | Ball decelerates toward minimum | Permanent |
| Multi-Ball | `2x` | Spawns a second ball | — |

A power-up is collected when the ball's rect overlaps it:

```python
def check_collect(self, ball_rect) -> PowerUp | None:
    for pu in self.active:
        if pu.alive and pu.rect.colliderect(ball_rect):
            pu.alive = False
            return pu
    return None
```

The collector is determined by ball direction:

```python
collector = 0 if ball.vx < 0 else 1   # moving left → P1 hit it
opponent  = 1 - collector
```

---

### Chapter 9 — Rendering Architecture

#### Surface Compositing

Each frame layers surfaces from back to front:

```
1. Background (static grid surface, blit once)
2. Power-ups
3. Particles
4. Paddles
5. Ball (trail → glow → core)
6. HUD (scores, names)
7. Pause overlay (if paused)
```

Using a pre-rendered `pygame.Surface` for the background avoids re-drawing the grid every frame.

#### Alpha Blending

Glow effects use `pygame.SRCALPHA` surfaces:

```python
glow = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
pygame.draw.circle(glow, (*color, alpha), (radius, radius), radius)
screen.blit(glow, (x - radius, y - radius))
```

#### Screen Shake

On a score, a random pixel offset is applied when blitting the background:

```python
if self.shake > 0:
    offset = (random.randint(-6, 6), random.randint(-6, 6))
    self.shake -= 1
screen.blit(self._bg, offset)
```

---

## 🛠️ Contributing

Contributions are welcome! Here are some ideas for extending the game:

- **Online Multiplayer** — use Python `socket` or `asyncio`
- **Leaderboard** — save high scores to a local JSON file
- **Custom Themes** — different neon colour palettes
- **Tournament Mode** — best of 3/5 sets
- **More Power-Ups** — teleport pads, curved ball, invisible ball
- **Sound Options** — volume slider, mute button in menu

### How to Contribute

```bash
# 1. Fork the repository on GitHub

# 2. Create a feature branch
git checkout -b feature/my-awesome-feature

# 3. Make your changes and commit
git add .
git commit -m "add my awesome feature"

# 4. Push and open a Pull Request
git push origin feature/my-awesome-feature
```

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

You are free to use, modify, and distribute this code for any purpose, including commercial projects, as long as you include the copyright notice.

---

## 🙏 Credits & Resources

- **[Pygame](https://www.pygame.org/)** — Python game development library
- **[NumPy](https://numpy.org/)** — Procedural audio synthesis
- **Game Design Inspiration** — Original Pong (Atari, 1972)
- **KawerifyTech** — Project development and design

---

<div align="center">

**Developed with ❤️ by [KawerifyTech](https://kawerifytech.com)**

🌐 [kawerifytech.com](https://kawerifytech.com) &nbsp;·&nbsp;
🐙 [GitHub](https://github.com/tonderaikawere/my-python-pong)

*Found this useful? Please ⭐ the repo — it helps more people find it!*

</div>
