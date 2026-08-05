from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel

from gui.components.window_header import WindowHeader
from gui.components.panel import Panel
from gui.translations import tr

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
    ("Author", "Francisco Rodrigues Oliveira"),
    ("GitHub", "https://github.com/francisco726/Aegis"),
)


class AboutWindow(QMainWindow):
    """Static project info screen.

    The field labels/values in ABOUT_FIELDS are project facts, not UI
    chrome, so (unlike the rest of the window) they are left untranslated
    on purpose — "Aegis", the license, the tech stack, etc. don't change
    meaning across languages.
    """

    about_window_closed = Signal()

    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self._setup_window()

    def _setup_window(self):
        lang = self.settings.language
        self.setWindowTitle(tr("about_title", lang))
        self.resize(1000, 700)

        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(16)

        header = WindowHeader(tr("about_title", lang))
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

            value_label = QLabel()
            value_label.setObjectName("StatusValue")
            value_label.setWordWrap(True)

            if label_text == "GitHub":
                value_label.setText(f'<a href="{value}">{value}</a>')
                value_label.setOpenExternalLinks(True)
                value_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
            else:
                value_label.setText(value)

            row.addWidget(label)
            row.addWidget(value_label, stretch=1)
            panel.add_layout(row)

        return panel

    def closeEvent(self, event):
        self.about_window_closed.emit()
        super().closeEvent(event)
