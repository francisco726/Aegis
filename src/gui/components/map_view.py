from PySide6.QtWidgets import QFrame
from PySide6.QtGui import QPainter, QColor, QPen, QBrush
from PySide6.QtCore import Qt


class MapView(QFrame):
    """Renders satellites and fires from a SimulationSnapshot on a simple
    latitude/longitude grid.

    This widget reads ONLY plain data already exposed by the domain
    (`snapshot.satellite`, `snapshot.fire`, `position.latitude/longitude`,
    `fire.intensity`). It makes no decisions about detection, alerts, or
    simulation state — it is a projection + draw step, nothing more. If the
    domain someday exposes richer entities (weather, other missions), this
    widget will need updating, but it will never need to know *why* an
    entity is where it is.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("MapView")
        self._snapshot = None

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

        margin = 20
        w = max(self.width() - 2 * margin, 1)
        h = max(self.height() - 2 * margin, 1)

        x = margin + max(0.0, min(1.0, x_ratio)) * w
        y = margin + max(0.0, min(1.0, y_ratio)) * h
        return x, y

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.fillRect(self.rect(), QColor("#0B1220"))

        pen = QPen(QColor("#1E293B"))
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
            radius = 6 + min(fire.intensity, 1.0) * 12
            color = QColor("#F59E0B") if fire.intensity < 0.75 else QColor("#EF4444")
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(int(x - radius / 2), int(y - radius / 2), int(radius), int(radius))

        for satellite in self._snapshot.satellite:
            x, y = self._project(satellite.position)
            painter.setBrush(QBrush(QColor("#3B82F6")))
            painter.setPen(QPen(QColor("#F8FAFC"), 1))
            painter.drawEllipse(int(x - 5), int(y - 5), 10, 10)

        painter.end()
