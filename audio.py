# audio.py — My Python Pong
# Developed by KawerifyTech | kawerifytech.com

import pygame

try:
    import numpy as np
    _HAS_NUMPY = True
except ImportError:
    _HAS_NUMPY = False

_SAMPLE_RATE = 44_100


def _make_tone(
    freq: float,
    duration: float,
    volume: float = 0.4,
    wave: str = "sine",
    attack: float = 0.01,
    decay: float = 0.10,
) -> pygame.mixer.Sound:
    """Synthesise a mono tone and return a pygame Sound (stereo)."""
    n = int(_SAMPLE_RATE * duration)

    if _HAS_NUMPY:
        t = np.linspace(0, duration, n, endpoint=False)

        if wave == "square":
            data = np.sign(np.sin(2 * np.pi * freq * t))
        elif wave == "triangle":
            data = 2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1
        elif wave == "saw":
            data = 2 * (t * freq - np.floor(t * freq + 0.5))
        else:  # sine (default)
            data = np.sin(2 * np.pi * freq * t)

        # Simple ADSR envelope (just A+D here)
        env   = np.ones(n)
        a_n   = min(int(attack * _SAMPLE_RATE), n)
        d_n   = min(int(decay  * _SAMPLE_RATE), n - a_n)
        if a_n:
            env[:a_n]            = np.linspace(0, 1, a_n)
        if d_n:
            env[n - d_n:]        = np.linspace(1, 0, d_n)

        data   = (data * env * volume * 32_767).astype(np.int16)
        stereo = np.column_stack([data, data])
        return pygame.sndarray.make_sound(stereo)
    else:
        # Silent fallback when numpy is absent
        return pygame.mixer.Sound(buffer=bytes(n * 4))


class AudioManager:
    """Manages all synthesised game sounds."""

    def __init__(self):
        self.enabled = True
        self._sounds: dict[str, pygame.mixer.Sound] = {}
        self._build()

    # ── Build sound library ───────────────────────────────────────────────────
    def _build(self) -> None:
        if not pygame.mixer.get_init():
            self.enabled = False
            return
        try:
            self._sounds = {
                "hit"   : _make_tone(380, 0.09, 0.45, "square",   0.003, 0.070),
                "wall"  : _make_tone(260, 0.07, 0.30, "triangle", 0.003, 0.050),
                "score" : _make_tone(740, 0.40, 0.50, "sine",     0.015, 0.350),
                "win"   : _make_tone(528, 0.80, 0.55, "sine",     0.025, 0.650),
                "pu"    : _make_tone(660, 0.18, 0.42, "triangle", 0.008, 0.140),
                "menu"  : _make_tone(196, 0.12, 0.28, "sine",     0.008, 0.090),
            }
        except Exception:
            self.enabled = False

    # ── Public API ────────────────────────────────────────────────────────────
    def play(self, name: str) -> None:
        if self.enabled and name in self._sounds:
            self._sounds[name].play()

    def toggle(self) -> None:
        self.enabled = not self.enabled
