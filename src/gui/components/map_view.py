import random

from PySide6.QtWidgets import QFrame
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath, QRadialGradient, QPixmap, QImage
from PySide6.QtCore import Qt, QRectF

try:
    import numpy as np
    from PIL import Image
    _NOISE_DEPS_AVAILABLE = True
except ImportError:
    _NOISE_DEPS_AVAILABLE = False


def _value_noise(width: int, height: int, seed: int, scales) -> "np.ndarray":
    """Fractal value noise: sum of several octaves of a small random grid,
    each upsampled with bilinear interpolation, coarsest-to-finest. This is
    what gives the terrain continuous, organic variation instead of the
    hard-edged "painted circles" look — the same family of technique real
    terrain generators use, just a minimal hand-rolled version so no extra
    dependency beyond numpy/Pillow (already needed for the Earth widget)."""
    rng = np.random.default_rng(seed)
    noise = np.zeros((height, width), dtype=np.float64)
    amplitude, total_amp = 1.0, 0.0

    for scale in scales:
        grid_w = max(2, width // scale)
        grid_h = max(2, height // scale)
        small = (rng.random((grid_h, grid_w)) * 255).astype(np.uint8)
        upsampled = Image.fromarray(small, mode="L").resize((width, height), Image.BILINEAR)
        noise += amplitude * (np.asarray(upsampled, dtype=np.float64) / 255.0)
        total_amp += amplitude
        amplitude *= 0.5

    return noise / total_amp


class MapView(QFrame):
    """Renders satellites and fires from a SimulationSnapshot over a
    procedurally generated terrain backdrop (green/brown patches with a
    grainy overlay, meant to read as "aerial/satellite view of land" —
    not a real, geographically accurate map of any specific place).

    This widget reads ONLY plain data already exposed by the domain
    (`snapshot.satellite`, `snapshot.fire`, `position.latitude/longitude`,
    `fire.intensity`). It makes no decisions about detection, alerts, or
    simulation state — it is a projection + draw step, nothing more.

    Both the terrain texture and the entity icons are drawn procedurally
    (QPainter paths/shapes), not loaded from external image files: no
    external asset dependency, and no risk of misrepresenting a real
    place's geography inaccurately.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("MapView")
        self._snapshot = None
        self._terrain_pixmap = None

        # Fixed bounds around the region used by Scenario(); a future version
        # could derive these dynamically from entity positions.
        self._lat_bounds = (41.40, 41.70)
        self._lon_bounds = (-8.60, -8.20)

    def update_snapshot(self, snapshot) -> None:
        self._snapshot = snapshot
        self.update()

    def _project(self, position):
        lat_min, lat_max = self._lat_bounds
        lon_min, lon_max = self._lon_bounds

        x_ratio = (position.longitude - lon_min) / (lon_max - lon_min)
        y_ratio = 1 - (position.latitude - lat_min) / (lat_max - lat_min)

        margin = 24
        w = max(self.width() - 2 * margin, 1)
        h = max(self.height() - 2 * margin, 1)

        x = margin + max(0.0, min(1.0, x_ratio)) * w
        y = margin + max(0.0, min(1.0, y_ratio)) * h
        return x, y

    # ---- terrain backdrop ----------------------------------------------
    def _generate_terrain_pixmap(self, width: int, height: int) -> QPixmap:
        """Builds the terrain texture once per size and caches it — this
        never re-runs mid-simulation just because a step repainted the
        widget, only when the widget is actually resized."""
        if _NOISE_DEPS_AVAILABLE:
            return self._generate_terrain_pixmap_noise(width, height)
        return self._generate_terrain_pixmap_blobs(width, height)

    def _generate_terrain_pixmap_noise(self, width: int, height: int) -> QPixmap:
        """Continuous, photo-like terrain: two independent noise fields
        (elevation, moisture) mapped through a vegetation/soil color ramp,
        with elevation-based shading and fine grain — much closer to an
        aerial/satellite composite than discrete shapes."""
        elevation = _value_noise(width, height, seed=11, scales=(64, 32, 16, 8))
        moisture = _value_noise(width, height, seed=42, scales=(96, 48, 20))

        index = np.clip(moisture * 0.65 + (1.0 - elevation) * 0.35, 0.0, 1.0)

        stops = [
            (0.00, np.array([38, 60, 33], dtype=np.float64)),   # dark forest green
            (0.30, np.array([64, 92, 48], dtype=np.float64)),   # mid green
            (0.50, np.array([104, 108, 58], dtype=np.float64)), # olive / dry grass
            (0.70, np.array([120, 92, 58], dtype=np.float64)),  # brown soil
            (1.00, np.array([150, 124, 84], dtype=np.float64)), # dry tan
        ]

        rgb = np.zeros((height, width, 3), dtype=np.float64)
        for (t0, c0), (t1, c1) in zip(stops[:-1], stops[1:]):
            mask = (index >= t0) & (index <= t1)
            span = (t1 - t0) or 1e-6
            local_t = (index[mask] - t0) / span
            for ch in range(3):
                rgb[..., ch][mask] = c0[ch] + (c1[ch] - c0[ch]) * local_t

        # gentle elevation-based shading, like a soft hillshade
        shade = 0.85 + 0.3 * (elevation - 0.5)
        rgb *= shade[..., None]

        # fine grain for a "photographed", not "painted", texture
        rng = np.random.default_rng(7)
        grain = (rng.random((height, width)) - 0.5) * 14
        rgb = np.clip(rgb + grain[..., None], 0, 255).astype(np.uint8)

        qimage = QImage(rgb.tobytes(), width, height, width * 3, QImage.Format_RGB888)
        return QPixmap.fromImage(qimage)

    def _generate_terrain_pixmap_blobs(self, width: int, height: int) -> QPixmap:
        """Fallback used only if numpy/Pillow aren't installed: simpler
        overlapping-ellipse terrain. Visually cruder than the noise-based
        version, but keeps the widget working with zero extra dependencies."""
        pixmap = QPixmap(width, height)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.fillRect(0, 0, width, height, QColor("#4A3C2A"))

        rng = random.Random(1234)
        patch_colors = [
            QColor(72, 94, 52, 235),
            QColor(90, 113, 64, 220),
            QColor(56, 76, 42, 215),
            QColor(108, 88, 58, 205),
            QColor(128, 104, 70, 195),
            QColor(64, 84, 48, 225),
        ]

        painter.setPen(Qt.NoPen)
        blob_count = max(1, int((width * height) / 2600))
        for _ in range(blob_count):
            cx = rng.uniform(-20, width + 20)
            cy = rng.uniform(-20, height + 20)
            rx = rng.uniform(20, 85)
            ry = rx * rng.uniform(0.55, 0.9)
            painter.setBrush(rng.choice(patch_colors))
            painter.drawEllipse(QRectF(cx - rx, cy - ry, rx * 2, ry * 2))

        painter.end()
        return pixmap

    # ---- icon drawing ------------------------------------------------
    def _draw_fire_icon(self, painter: QPainter, x: float, y: float, intensity: float):
        size = 14 + min(max(intensity, 0.0), 1.0) * 10

        path = QPainterPath()
        path.moveTo(x, y + size * 0.55)
        path.cubicTo(
            x - size * 0.5, y + size * 0.15,
            x - size * 0.32, y - size * 0.55,
            x + size * 0.02, y - size * 0.95,
        )
        path.cubicTo(
            x + size * 0.22, y - size * 0.55,
            x + size * 0.05, y - size * 0.35,
            x + size * 0.28, y - size * 0.30,
        )
        path.cubicTo(
            x + size * 0.55, y - size * 0.05,
            x + size * 0.4, y + size * 0.35,
            x, y + size * 0.55,
        )
        path.closeSubpath()

        gradient = QRadialGradient(x, y - size * 0.1, size)
        outer = QColor("#DC2626") if intensity >= 0.75 else QColor("#F59E0B")
        gradient.setColorAt(0.0, QColor("#FDE68A"))
        gradient.setColorAt(0.55, QColor("#F59E0B"))
        gradient.setColorAt(1.0, outer)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(gradient))
        painter.drawPath(path)

    def _draw_satellite_icon(self, painter: QPainter, x: float, y: float):
        size = 20

        painter.save()
        painter.translate(x, y)

        body_size = size * 0.42
        wing_w = size * 0.62
        wing_h = size * 0.34

        panel_pen = QPen(QColor("#1D4ED8"), 1)
        panel_brush = QBrush(QColor("#60A5FA"))
        painter.setPen(panel_pen)
        painter.setBrush(panel_brush)

        left_wing = QRectF(-body_size / 2 - wing_w, -wing_h / 2, wing_w, wing_h)
        right_wing = QRectF(body_size / 2, -wing_h / 2, wing_w, wing_h)
        painter.drawRect(left_wing)
        painter.drawRect(right_wing)

        # panel grid lines, purely decorative
        for wing in (left_wing, right_wing):
            for i in range(1, 3):
                lx = wing.left() + wing.width() * i / 3
                painter.drawLine(int(lx), int(wing.top()), int(lx), int(wing.bottom()))

        # body
        painter.setPen(QPen(QColor("#1E293B"), 1))
        painter.setBrush(QBrush(QColor("#F8FAFC")))
        painter.drawRect(QRectF(-body_size / 2, -body_size / 2, body_size, body_size))

        # antenna
        painter.setPen(QPen(QColor("#94A3B8"), 1))
        painter.drawLine(0, int(-body_size / 2), 0, int(-body_size / 2 - size * 0.28))

        painter.restore()

    # ---- painting -----------------------------------------------------
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width, height = max(self.width(), 1), max(self.height(), 1)
        if self._terrain_pixmap is None or self._terrain_pixmap.size().width() != width \
                or self._terrain_pixmap.size().height() != height:
            self._terrain_pixmap = self._generate_terrain_pixmap(width, height)

        painter.drawPixmap(0, 0, self._terrain_pixmap)

        # Slight darkening so satellite/fire icons and the grid stay legible
        # regardless of how bright the terrain patch underneath them is.
        painter.fillRect(self.rect(), QColor(0, 0, 0, 70))

        pen = QPen(QColor(255, 255, 255, 30))
        painter.setPen(pen)
        step = 40
        for x in range(0, self.width(), step):
            painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), step):
            painter.drawLine(0, y, self.width(), y)

        if self._snapshot is None:
            painter.end()
            return

        for fire in self._snapshot.fire:
            x, y = self._project(fire.position)
            self._draw_fire_icon(painter, x, y, fire.intensity)

        for satellite in self._snapshot.satellite:
            x, y = self._project(satellite.position)
            self._draw_satellite_icon(painter, x, y)

        painter.end()
