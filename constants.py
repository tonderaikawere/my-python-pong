# constants.py — My Python Pong
# Developed by KawerifyTech | kawerifytech.com

# ── Identity ──────────────────────────────────────────────────────────────────
GAME_TITLE  = "My Python Pong"
VERSION     = "1.0.0"
DEVELOPER   = "KawerifyTech"
WEBSITE     = "kawerifytech.com"
GITHUB      = "github.com/tonderaikawere/my-python-pong"

# ── Screen ────────────────────────────────────────────────────────────────────
WIDTH  = 1280
HEIGHT = 720
FPS    = 60

# ── Colors (neon dark theme) ──────────────────────────────────────────────────
BLACK       = (0,   0,   0  )
WHITE       = (255, 255, 255)
NEON_CYAN   = (0,   230, 255)
NEON_GREEN  = (57,  255, 20 )
NEON_PINK   = (255, 20,  147)
NEON_YELLOW = (255, 230, 0  )
NEON_ORANGE = (255, 140, 0  )
NEON_PURPLE = (180, 0,   255)
DIM_WHITE   = (180, 180, 200)
BG_COLOR    = (5,   5,   18 )
GRID_COLOR  = (18,  18,  40 )
MID_COLOR   = (28,  28,  60 )

P1_COLOR    = NEON_CYAN
P2_COLOR    = NEON_PINK

# ── Paddle ────────────────────────────────────────────────────────────────────
PADDLE_W      = 14
PADDLE_H      = 100
PADDLE_SPEED  = 7
PADDLE_MARGIN = 36

# ── Ball ──────────────────────────────────────────────────────────────────────
BALL_SIZE       = 14
BALL_INIT_SPEED = 6
BALL_MAX_SPEED  = 20
BALL_SPEED_INC  = 0.28
TRAIL_LENGTH    = 24

# ── Scoring ───────────────────────────────────────────────────────────────────
WIN_SCORE = 7

# ── Power-ups ─────────────────────────────────────────────────────────────────
POWERUP_SIZE     = 26
POWERUP_DURATION = 8_000   # ms
POWERUP_INTERVAL = 12_000  # ms between spawns

# ── Particles ─────────────────────────────────────────────────────────────────
MAX_PARTICLES = 300

# ── AI difficulty (tracking accuracy 0.0 → 1.0) ───────────────────────────────
AI_EASY   = 0.30
AI_MEDIUM = 0.65
AI_HARD   = 0.95

# ── Game States ───────────────────────────────────────────────────────────────
STATE_SPLASH  = "splash"
STATE_MENU    = "menu"
STATE_MODE    = "mode"
STATE_PLAYING = "playing"
STATE_PAUSED  = "paused"
STATE_WIN     = "win"
