from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QSlider,
)

from gui.components.window_header import WindowHeader
from gui.components.panel import Panel


class SettingsWindow(QMainWindow):
    """Placeholder settings screen.

    Every control here is intentionally disabled — nothing is wired to real
    behaviour yet. The point of building the layout now is so the structure
    (grouped rows inside a Panel) doesn't need to be redesigned once a
    setting actually does something; only `setEnabled(True)` and a signal
    connection will need to be added later.
    """

    settings_window_closed = Signal()

    def __init__(self):
        super().__init__()
        self._setup_window()

    def _setup_window(self):
        self.setWindowTitle("Settings")
        self.resize(1000, 700)

        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(18)

        header = WindowHeader("Settings")
        root.addWidget(header)

        content = QVBoxLayout()
        content.setContentsMargins(24, 0, 24, 24)
        content.addWidget(self._create_settings_panel())
        content.addStretch()
        root.addLayout(content, stretch=1)

        header.back_button.clicked.connect(self.close)

    def _create_settings_panel(self):
        panel = Panel()

        theme_box = QComboBox()
        theme_box.addItems(["Dark", "Light"])

        language_box = QComboBox()
        language_box.addItems(["English", "Português"])

        speed_slider = QSlider(Qt.Horizontal)
        speed_slider.setRange(1, 10)
        speed_slider.setValue(5)

        units_box = QComboBox()
        units_box.addItems(["Metric", "Imperial"])

        for label_text, control in (
            ("Theme", theme_box),
            ("Language", language_box),
            ("Simulation Speed", speed_slider),
            ("Units", units_box),
        ):
            panel.add_layout(self._labeled_row(label_text, control))

        return panel

    def _labeled_row(self, label_text: str, control):
        row = QHBoxLayout()
        row.setContentsMargins(0, 4, 0, 4)

        label = QLabel(label_text)
        label.setObjectName("StatusLabel")
        label.setFixedWidth(160)

        control.setEnabled(False)  # not functional yet

        row.addWidget(label)
        row.addWidget(control, stretch=1)
        return row

    def closeEvent(self, event):
        self.settings_window_closed.emit()
        super().closeEvent(event)
