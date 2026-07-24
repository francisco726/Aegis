from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel

from gui.components.window_header import WindowHeader
from gui.components.panel import Panel

ABOUT_FIELDS = (
    ("Name", "Aegis"),
    (
        "Description",
        "Modular aerospace simulation platform for satellite-based "
        "monitoring missions (Forest Fire today, more missions planned).",
    ),
    ("Version", "0.1.0 — Forest Fire Mission"),
    ("Technologies", "Python, PySide6 (Qt), Domain-Driven Design"),
    (
        "Objective",
        "Portfolio project demonstrating software architecture, clean "
        "domain design and professional interface engineering.",
    ),
    ("License", "MIT"),
    ("Author", "TODO: add your name"),
    ("GitHub", "TODO: add repository link"),
)


class AboutWindow(QMainWindow):
    about_window_closed = Signal()

    def __init__(self):
        super().__init__()
        self._setup_window()

    def _setup_window(self):
        self.setWindowTitle("About")
        self.resize(1000, 700)

        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(18)

        header = WindowHeader("About Aegis")
        root.addWidget(header)

        content = QVBoxLayout()
        content.setContentsMargins(24, 0, 24, 24)
        content.addWidget(self._create_info_panel())
        content.addStretch()
        root.addLayout(content, stretch=1)

        header.back_button.clicked.connect(self.close)

    def _create_info_panel(self):
        panel = Panel()

        for label_text, value in ABOUT_FIELDS:
            row = QHBoxLayout()

            label = QLabel(label_text)
            label.setObjectName("StatusLabel")
            label.setFixedWidth(140)

            value_label = QLabel(value)
            value_label.setObjectName("StatusValue")
            value_label.setWordWrap(True)

            row.addWidget(label)
            row.addWidget(value_label, stretch=1)
            panel.add_layout(row)

        return panel

    def closeEvent(self, event):
        self.about_window_closed.emit()
        super().closeEvent(event)
