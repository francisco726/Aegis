from PySide6.QtCore import Qt
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
from gui.components.panel import Panel
from gui.components.section_header import SectionHeader
from gui.components.starfield_widget import StarfieldWidget

from domain.scenario import Scenario
from domain.simulation import Simulation


class HomeWindow(QMainWindow):
    """Application entry screen and navigation controller.

    HomeWindow is the only window that knows about the other windows.
    It creates them, shows them, and listens for their "closed" Signal to
    reappear — the child windows never import HomeWindow back.

    HomeWindow is also where a mission's domain objects are assembled
    (Scenario -> World -> Simulation) before being handed, already built,
    to the mission window. HomeWindow does not interpret or use anything
    inside those objects itself; it only constructs and passes them along.
    """

    def __init__(self):
        super().__init__()
        self._setup_window()

    # ---- setup ------------------------------------------------------
    def _setup_window(self):
        self.setWindowTitle("Aegis")
        self.resize(1200, 800)

        central = QWidget()
        self.setCentralWidget(central)

        self._background = StarfieldWidget(parent=central)
        self._background.setGeometry(0, 0, self.width(), self.height())
        self._background.lower()

        root = QVBoxLayout(central)
        root.setContentsMargins(48, 40, 48, 32)
        root.setSpacing(24)

        root.addLayout(self._create_hero())
        root.addWidget(self._create_divider())
        root.addLayout(self._create_body(), stretch=1)
        root.addLayout(self._create_footer())

        self._connect_signals()

    def _create_hero(self):
        hero = QVBoxLayout()
        hero.setSpacing(6)

        title = QLabel("AEGIS")
        title.setObjectName("AppTitle")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Modular Aerospace Simulation Platform")
        subtitle.setObjectName("AppSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        hero.addWidget(title)
        hero.addWidget(subtitle)
        return hero

    def _create_divider(self) -> QFrame:
        divider = QFrame()
        divider.setObjectName("HeroDivider")
        divider.setFixedHeight(1)
        return divider

    def _create_body(self):
        body = QHBoxLayout()
        body.setSpacing(24)
        body.addLayout(self._create_mission_column(), stretch=3)
        body.addLayout(self._create_general_column(), stretch=1)
        return body

    def _create_mission_column(self):
        column = QVBoxLayout()
        column.setSpacing(10)
        column.addWidget(SectionHeader("Mission"))

        self.mission_panel = Panel()
        self.fire_button = QPushButton("Forest Fire Mission")
        self.fire_button.setObjectName("MissionCardButton")
        self.fire_button.setFixedHeight(56)
        self.mission_panel.add_widget(self.fire_button)

        placeholder = QLabel("More missions coming soon...")
        placeholder.setObjectName("MutedLabel")
        placeholder.setAlignment(Qt.AlignCenter)
        self.mission_panel.add_widget(placeholder)

        column.addWidget(self.mission_panel)
        column.addStretch()
        return column

    def _create_general_column(self):
        column = QVBoxLayout()
        column.setSpacing(10)
        column.addWidget(SectionHeader("General"))

        self.general_panel = Panel()
        self.settings_button = QPushButton("Settings")
        self.about_button = QPushButton("About")

        for button in (self.settings_button, self.about_button):
            button.setObjectName("NavButton")
            button.setFixedHeight(44)
            self.general_panel.add_widget(button)

        column.addWidget(self.general_panel)
        column.addStretch()
        return column

    def _create_footer(self):
        footer = QHBoxLayout()
        footer.addStretch()

        self.quit_button = QPushButton("Quit")
        self.quit_button.setObjectName("DangerButton")
        self.quit_button.setFixedSize(140, 40)

        footer.addWidget(self.quit_button)
        return footer

    def _connect_signals(self):
        self.fire_button.clicked.connect(self.open_fire_mission)
        self.settings_button.clicked.connect(self.open_settings_window)
        self.about_button.clicked.connect(self.open_about_window)
        self.quit_button.clicked.connect(self.close)

    # ---- navigation ---------------------------------------------------
    def open_fire_mission(self):
        scenario = Scenario()
        world = scenario.create_world()
        simulation = Simulation(world)

        self.fire_window = FireMissionWindow(simulation)
        self.fire_window.fire_mission_closed.connect(self.show)

        self.hide()
        self.fire_window.show()

    def open_settings_window(self):
        self.settings_window = SettingsWindow()
        self.settings_window.settings_window_closed.connect(self.show)

        self.hide()
        self.settings_window.show()

    def open_about_window(self):
        self.about_window = AboutWindow()
        self.about_window.about_window_closed.connect(self.show)

        self.hide()
        self.about_window.show()

    # ---- misc -----------------------------------------------------------
    def resizeEvent(self, event):
        self._background.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)
