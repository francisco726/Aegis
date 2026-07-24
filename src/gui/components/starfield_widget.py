import random

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QRadialGradient, QBrush
from PySide6.QtCore import Qt


class StarfieldWidget(QWidget):
    """Purely decorative background: a soft radial glow plus a scattered
    field of static points, standing in for the "imagem espacial" element
    of the Home screen mockup without depending on an external image asset.

    No simulation/domain dependency whatsoever — this is presentation only,
    and it never intercepts mouse events (it sits behind real widgets).
    """

    def __init__(self, star_count: int = 160, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        rng = random.Random(42)  # fixed seed: stable layout across resizes
        self._stars = [
            (rng.random(), rng.random(), rng.uniform(0.6, 2.4), rng.uniform(0.2, 0.9))
            for _ in range(star_count)
        ]

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width, height = self.width(), self.height()

        glow = QRadialGradient(width * 0.5, height * 0.3, max(width, height) * 0.7)
        glow.setColorAt(0.0, QColor(37, 99, 235, 35))
        glow.setColorAt(1.0, QColor(15, 23, 42, 0))
        painter.fillRect(self.rect(), QBrush(glow))

        painter.setPen(Qt.NoPen)
        for rel_x, rel_y, radius, alpha in self._stars:
            color = QColor(248, 250, 252)
            color.setAlphaF(alpha)
            painter.setBrush(color)
            painter.drawEllipse(int(rel_x * width), int(rel_y * height), int(radius), int(radius))
