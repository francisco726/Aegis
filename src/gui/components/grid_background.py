from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Qt


class GridBackgroundWidget(QWidget):
    """A faint technical grid used as the Home screen's background accent.

    This replaces an earlier space/starfield background. A quiet grid —
    the same visual language as the Simulation View's map grid — reads as
    engineering/CAD tooling and keeps the app's few decorative touches
    consistent with each other, rather than reaching for a "landing page"
    flourish that doesn't belong in professional desktop software.

    Purely presentational; no domain dependency, never intercepts input.
    """

    def __init__(self, spacing: int = 32, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self._spacing = spacing
        self._line_color = QColor(148, 163, 184, 30)

    def set_line_color(self, color: QColor) -> None:
        self._line_color = color
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(self._line_color, 1))

        for x in range(0, self.width(), self._spacing):
            painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), self._spacing):
            painter.drawLine(0, y, self.width(), y)
