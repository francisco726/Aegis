"""
Rotating Earth background widget for the Home screen.

This renders a small, slowly-rotating globe from a REAL equirectangular
Earth texture the user supplies — not a hand-drawn stand-in. A good, free,
public-domain source is NASA's "Blue Marble" imagery:
https://visibleearth.nasa.gov/collection/1484/blue-marble

No texture ships with this project: this sandbox's network access is
restricted to package registries (PyPI, npm, GitHub...), not general
image hosts, so the code itself cannot fetch one. A procedurally drawn
"cartoon" continent shape would look worse than no globe at all for a
portfolio piece, so this module simply does nothing until a real texture
is present.

Drop a texture at TEXTURE_PATH (see below) and this widget activates
automatically. HomeWindow checks `RotatingEarthWidget.is_available()` and
falls back to the existing GridBackgroundWidget if it isn't.

How the rotation is faked convincingly: on first use, this module takes
the flat equirectangular image and mathematically projects it — true
orthographic sphere projection, with the correct curvature and edge
foreshortening a photo of a globe would have, not just a horizontal pan —
into FRAME_COUNT still frames, one per rotation angle. Frames are cached
as PNGs next to the source texture, so this (the only computationally
expensive part) runs once total, not once per app launch. After that,
the widget just cycles cached frames on a QTimer.
"""

import math
import os

from PySide6.QtCore import Qt, QTimer, QRect
from PySide6.QtGui import QPainter, QPixmap, QImage, QColor
from PySide6.QtWidgets import QWidget

try:
    import numpy as np
    from PIL import Image
    _DEPENDENCIES_AVAILABLE = True
except ImportError:
    _DEPENDENCIES_AVAILABLE = False


ASSETS_DIR = os.path.join("gui", "assets")
TEXTURE_PATH = os.path.join(ASSETS_DIR, "earth_equirectangular.jpg")
FRAMES_DIR = os.path.join(ASSETS_DIR, "earth_frames")

FRAME_COUNT = 72
FRAME_SIZE = 420
ROTATION_PERIOD_MS = 26_000
STAR_COUNT = 90


def _frame_path(index: int) -> str:
    return os.path.join(FRAMES_DIR, f"frame_{index:03d}.png")


def _frames_are_cached() -> bool:
    return all(os.path.exists(_frame_path(i)) for i in range(FRAME_COUNT))


def _generate_frames() -> None:
    """Project the equirectangular texture into FRAME_COUNT orthographic
    sphere views (one per rotation step) and cache them as PNGs.

    Orthographic inverse projection, viewed straight-on at the equator
    (lat0 = 0), which simplifies the general formula to:
        lat = asin(y)
        lon = lon0 + atan2(x, sqrt(1 - x^2 - y^2))
    for a view-plane point (x, y) with x^2+y^2 <= 1. A cosine-based
    darkening toward the limb approximates the subtle shading a real
    photograph of a sphere has at its edge.
    """
    os.makedirs(FRAMES_DIR, exist_ok=True)

    source = Image.open(TEXTURE_PATH).convert("RGB")
    src = np.asarray(source, dtype=np.float32) / 255.0
    src_h, src_w, _ = src.shape

    size = FRAME_SIZE
    radius = size / 2.0

    y_idx, x_idx = np.mgrid[0:size, 0:size].astype(np.float64)
    x = (x_idx - radius + 0.5) / radius
    y = -(y_idx - radius + 0.5) / radius  # flip so north is up on screen

    rho2 = x ** 2 + y ** 2
    inside = rho2 <= 1.0
    rho2_clamped = np.clip(rho2, 0, 1)
    cos_c = np.sqrt(1.0 - rho2_clamped)

    lat = np.arcsin(np.clip(y, -1.0, 1.0))

    for frame_index in range(FRAME_COUNT):
        lon0 = 2 * math.pi * frame_index / FRAME_COUNT
        lon = lon0 + np.arctan2(x, cos_c)

        u = ((lon + math.pi) / (2 * math.pi)) % 1.0
        v = np.clip(0.5 - lat / math.pi, 0.0, 1.0)

        sx = np.clip((u * src_w).astype(np.int32), 0, src_w - 1)
        sy = np.clip((v * src_h).astype(np.int32), 0, src_h - 1)

        rgb = src[sy, sx]

        # Subtle limb darkening for a more convincing sense of curvature.
        shade = np.clip(cos_c, 0.2, 1.0) ** 0.6
        rgb = rgb * shade[..., None]

        frame = np.zeros((size, size, 4), dtype=np.uint8)
        frame[..., 0:3] = np.clip(rgb * 255, 0, 255).astype(np.uint8)
        frame[..., 3] = np.where(inside, 255, 0).astype(np.uint8)

        Image.fromarray(frame, mode="RGBA").save(_frame_path(frame_index))


class RotatingEarthWidget(QWidget):
    """Displays a slowly rotating globe (cached frame sequence) plus a
    sparse, small starfield. Purely decorative, no domain dependency."""

    @staticmethod
    def is_available() -> bool:
        """Whether a real texture is present (and dependencies installed)
        so HomeWindow can decide whether to use this or the fallback grid."""
        return _DEPENDENCIES_AVAILABLE and os.path.exists(TEXTURE_PATH)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        if not _frames_are_cached():
            _generate_frames()

        self._frames = [QPixmap(_frame_path(i)) for i in range(FRAME_COUNT)]
        self._frame_index = 0

        import random
        rng = random.Random(7)
        self._stars = [
            (rng.random(), rng.random(), rng.uniform(0.5, 1.6), rng.uniform(0.25, 0.8))
            for _ in range(STAR_COUNT)
        ]

        self._timer = QTimer(self)
        self._timer.setInterval(max(1, ROTATION_PERIOD_MS // FRAME_COUNT))
        self._timer.timeout.connect(self._advance_frame)
        self._timer.start()

    def _advance_frame(self) -> None:
        self._frame_index = (self._frame_index + 1) % FRAME_COUNT
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(Qt.NoPen)
        for rel_x, rel_y, size, alpha in self._stars:
            color = QColor(232, 232, 232)
            color.setAlphaF(alpha)
            painter.setBrush(color)
            painter.drawEllipse(
                int(rel_x * self.width()), int(rel_y * self.height()),
                int(size), int(size),
            )

        pixmap = self._frames[self._frame_index]
        if not pixmap.isNull():
            target_size = min(self.width(), self.height()) * 0.55
            target_size = max(target_size, 1)
            x = self.width() - target_size * 0.65
            y = self.height() * 0.5 - target_size * 0.5
            painter.drawPixmap(
                QRect(int(x), int(y), int(target_size), int(target_size)),
                pixmap,
                pixmap.rect(),
            )
