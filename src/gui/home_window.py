from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
)

from gui.fire_mission_window import FireMissionWindow
from gui.settings_window import SettingsWindow
from gui.about_window import AboutWindow
from gui.coming_soon_window import ComingSoonWindow
from gui.components.panel import Panel
from gui.components.section_header import SectionHeader
from gui.components.grid_background import GridBackgroundWidget
from gui.components.rotating_earth import RotatingEarthWidget
from gui.components.status_bar import StatusBar
from gui.translations import tr
from gui.theme import DarkPalette, LightPalette

from domain.scenario import Scenario
from domain.simulation import Simulation


class HomeWindow(QMainWindow):
    """Application entry screen and navigation controller.

    HomeWindow is the only window that knows about the other windows. It
    creates them, shows them, and listens for their "closed" Signal to
    reappear — the child windows never import HomeWindow back.

    HomeWindow also owns the single AppSettings instance for its whole
    lifetime and passes it to every window it opens, so Theme/Language/
    Simulation Speed/Units stay one shared, live-updating source of truth
    instead of separate per-window state.
    """

    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self._setup_window()
        self._connect_settings()

    # ---- setup ------------------------------------------------------
    def _setup_window(self):
        self.setWindowTitle("Aegis")
        self.resize(1200, 800)

        central = QWidget()
        self.setCentralWidget(central)

        if RotatingEarthWidget.is_available():
            self._background = RotatingEarthWidget(parent=central)
        else:
            self._background = GridBackgroundWidget(parent=central)
            self._apply_background_color()
        self._background.setGeometry(0, 0, self.width(), self.height())
        self._background.lower()

        outer = QVBoxLayout(central)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        root = QVBoxLayout()
        root.setContentsMargins(48, 40, 48, 32)
        root.setSpacing(24)

        root.addLayout(self._create_hero())
        root.addWidget(self._create_divider())
        root.addLayout(self._create_body(), stretch=1)
        root.addLayout(self._create_footer())

        outer.addLayout(root, stretch=1)

        self.status_bar = StatusBar()
        self.status_bar.set_text(f"Aegis v0.1.0  ·  {tr('forest_fire_mission', self.settings.language)}")
        outer.addWidget(self.status_bar)

        self._connect_signals()

    def _create_hero(self):
        hero = QVBoxLayout()
        hero.setSpacing(4)

        self.title_label = QLabel("AEGIS")
        self.title_label.setObjectName("AppTitle")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.subtitle_label = QLabel(tr("app_subtitle", self.settings.language))
        self.subtitle_label.setObjectName("AppSubtitle")
        self.subtitle_label.setAlignment(Qt.AlignCenter)

        hero.addWidget(self.title_label)
        hero.addWidget(self.subtitle_label)
        return hero

    def _create_divider(self) -> QFrame:
        divider = QFrame()
        divider.setObjectName("HeroDivider")
        divider.setFixedHeight(1)
        return divider

    def _create_body(self):
        body = QHBoxLayout()
        body.setSpacing(20)
        body.addLayout(self._create_mission_column(), stretch=3)
        body.addLayout(self._create_general_column(), stretch=1)
        return body

    def _create_mission_column(self):
        lang = self.settings.language
        column = QVBoxLayout()
        column.setSpacing(8)

        self.mission_header = SectionHeader(tr("mission", lang))
        column.addWidget(self.mission_header)

        self.mission_panel = Panel()
        self.fire_button = QPushButton(tr("forest_fire_mission", lang))
        self.fire_button.setObjectName("MissionCardButton")
        self.fire_button.setFixedHeight(42)
        self.mission_panel.add_widget(self.fire_button)

        self.more_missions_label = QLabel(tr("more_missions", lang))
        self.more_missions_label.setObjectName("MutedLabel")
        self.more_missions_label.setAlignment(Qt.AlignCenter)
        self.mission_panel.add_widget(self.more_missions_label)

        column.addWidget(self.mission_panel)
        column.addStretch()
        return column

    def _create_general_column(self):
        lang = self.settings.language
        column = QVBoxLayout()
        column.setSpacing(8)

        self.general_header = SectionHeader(tr("general", lang))
        column.addWidget(self.general_header)

        self.general_panel = Panel()
        self.settings_button = QPushButton(tr("settings", lang))
        self.about_button = QPushButton(tr("about", lang))
        self.coming_soon_button = QPushButton(tr("coming_soon", lang))

        for button in (self.settings_button, self.about_button, self.coming_soon_button):
            button.setObjectName("NavButton")
            button.setFixedHeight(36)
            self.general_panel.add_widget(button)

        column.addWidget(self.general_panel)
        column.addStretch()
        return column

    def _create_footer(self):
        footer = QHBoxLayout()
        footer.addStretch()

        self.quit_button = QPushButton(tr("quit", self.settings.language))
        self.quit_button.setObjectName("DangerButton")
        self.quit_button.setFixedSize(120, 34)
        self.quit_button.clicked.connect(self.close)

        footer.addWidget(self.quit_button)
        return footer

    def _connect_signals(self):
        self.fire_button.clicked.connect(self.open_fire_mission)
        self.settings_button.clicked.connect(self.open_settings_window)
        self.about_button.clicked.connect(self.open_about_window)
        self.coming_soon_button.clicked.connect(self.open_coming_soon_window)

    def _connect_settings(self):
        self.settings.language_changed.connect(self._retranslate_ui)
        self.settings.theme_changed.connect(lambda _: self._apply_background_color())

    # ---- live language update -------------------------------------------
    def _retranslate_ui(self, lang: str):
        self.title_label.setText("AEGIS")
        self.subtitle_label.setText(tr("app_subtitle", lang))
        self.mission_header.setText(tr("mission", lang).upper())
        self.fire_button.setText(tr("forest_fire_mission", lang))
        self.more_missions_label.setText(tr("more_missions", lang))
        self.general_header.setText(tr("general", lang).upper())
        self.settings_button.setText(tr("settings", lang))
        self.about_button.setText(tr("about", lang))
        self.coming_soon_button.setText(tr("coming_soon", lang))
        self.quit_button.setText(tr("quit", lang))
        self.status_bar.set_text(f"Aegis v0.1.0  ·  {tr('forest_fire_mission', lang)}")

    def _apply_background_color(self):
        if not isinstance(self._background, GridBackgroundWidget):
            return
        palette = LightPalette if self.settings.theme == "light" else DarkPalette
        r, g, b = QColor(palette.TEXT_SECONDARY).getRgb()[:3]
        self._background.set_line_color(QColor(r, g, b, 35))

    # ---- navigation ---------------------------------------------------
    def open_fire_mission(self):
        scenario = Scenario()
        world = scenario.create_world()
        simulation = Simulation(world)

        self.fire_window = FireMissionWindow(simulation, self.settings)
        self.fire_window.fire_mission_closed.connect(self.show)

        self.hide()
        self.fire_window.show()

    def open_settings_window(self):
        self.settings_window = SettingsWindow(self.settings)
        self.settings_window.settings_window_closed.connect(self.show)

        self.hide()
        self.settings_window.show()

    def open_about_window(self):
        self.about_window = AboutWindow(self.settings)
        self.about_window.about_window_closed.connect(self.show)

        self.hide()
        self.about_window.show()

    def open_coming_soon_window(self):
        self.coming_soon_window = ComingSoonWindow(self.settings)
        self.coming_soon_window.coming_soon_closed.connect(self.show)

        self.hide()
        self.coming_soon_window.show()

    # ---- misc -----------------------------------------------------------
    def resizeEvent(self, event):
        self._background.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)
