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
from gui.translations import tr


class SettingsWindow(QMainWindow):
    """Settings screen, wired to a shared AppSettings instance.

    Every control here reads its initial value from `settings` and writes
    changes straight back to it — this window holds no preference state of
    its own. Other windows (Home, Fire Mission) already listen to
    `settings`'s change signals, so a change made here is visible
    immediately, including in windows currently open behind this one.
    """

    settings_window_closed = Signal()

    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self._setup_window()

    def _setup_window(self):
        lang = self.settings.language
        self.setWindowTitle(tr("settings", lang))
        self.resize(1000, 700)

        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(16)

        header = WindowHeader(tr("settings", lang))
        root.addWidget(header)

        content = QVBoxLayout()
        content.setContentsMargins(24, 0, 24, 24)
        content.addWidget(self._create_settings_panel())
        content.addStretch()
        root.addLayout(content, stretch=1)

        header.back_button.clicked.connect(self.close)

    def _create_settings_panel(self):
        lang = self.settings.language
        panel = Panel()

        panel.add_layout(self._create_theme_row(lang))
        panel.add_layout(self._create_language_row(lang))
        panel.add_layout(self._create_speed_row(lang))
        panel.add_layout(self._create_units_row(lang))

        return panel

    # ---- individual rows --------------------------------------------
    def _create_theme_row(self, lang):
        box = QComboBox()
        box.addItems([tr("dark", lang), tr("light", lang)])
        box.setCurrentIndex(0 if self.settings.theme == "dark" else 1)
        box.currentIndexChanged.connect(
            lambda index: self.settings.set_theme("dark" if index == 0 else "light")
        )
        return self._labeled_row(tr("theme", lang), box)

    def _create_language_row(self, lang):
        box = QComboBox()
        box.addItems(["English", "Português"])
        box.setCurrentIndex(0 if self.settings.language == "en" else 1)
        box.currentIndexChanged.connect(
            lambda index: self.settings.set_language("en" if index == 0 else "pt")
        )
        return self._labeled_row(tr("language", lang), box)

    def _create_speed_row(self, lang):
        row = QHBoxLayout()
        row.setContentsMargins(0, 4, 0, 4)

        label = QLabel(tr("simulation_speed", lang))
        label.setObjectName("StatusLabel")
        label.setFixedWidth(160)

        slider = QSlider(Qt.Horizontal)
        slider.setRange(1, 10)
        slider.setValue(round(self.settings.simulation_speed * 5))

        value_label = QLabel(f"{self.settings.simulation_speed:.1f}x")
        value_label.setObjectName("StatusValue")
        value_label.setFixedWidth(42)

        def on_change(value):
            multiplier = value / 5.0
            value_label.setText(f"{multiplier:.1f}x")
            self.settings.set_simulation_speed(multiplier)

        slider.valueChanged.connect(on_change)

        row.addWidget(label)
        row.addWidget(slider, stretch=1)
        row.addWidget(value_label)
        return row

    def _create_units_row(self, lang):
        box = QComboBox()
        box.addItems([tr("metric", lang), tr("imperial", lang)])
        box.setCurrentIndex(0 if self.settings.units == "metric" else 1)
        box.currentIndexChanged.connect(
            lambda index: self.settings.set_units("metric" if index == 0 else "imperial")
        )
        return self._labeled_row(tr("units", lang), box)

    def _labeled_row(self, label_text: str, control):
        row = QHBoxLayout()
        row.setContentsMargins(0, 4, 0, 4)

        label = QLabel(label_text)
        label.setObjectName("StatusLabel")
        label.setFixedWidth(160)

        row.addWidget(label)
        row.addWidget(control, stretch=1)
        return row

    def closeEvent(self, event):
        self.settings_window_closed.emit()
        super().closeEvent(event)
