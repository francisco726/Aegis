from PySide6.QtCore import Signal, QTimer, Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QComboBox,
    QStackedWidget,
    QListWidget,
    QListWidgetItem,
    QDoubleSpinBox,
)

from gui.components.window_header import WindowHeader
from gui.components.panel import Panel
from gui.components.status_row import StatusRow
from gui.components.section_header import SectionHeader
from gui.components.map_view import MapView
from gui.translations import tr

from domain.simulation_state import Simulationstate
from domain.satellite import Satellite
from domain.sensor import Sensor
from domain.fire import Fire
from domain.position import Position


BASE_STEP_INTERVAL_MS = 800
MIN_STEP_INTERVAL_MS = 60

DEFAULT_LATITUDE = 41.55
DEFAULT_LONGITUDE = -8.42
DEFAULT_SATELLITE_ALTITUDE = 700_000
DEFAULT_SENSOR_FOV = 15.0
DEFAULT_LAT_SPEED = 0.0001
DEFAULT_LON_SPEED = 0.0010
DEFAULT_FIRE_INTENSITY = 1.0
DEFAULT_FIRE_RADIUS = 10
DEFAULT_FIRE_SPREAD_RATE = 8


def format_altitude(altitude_m: float, units: str) -> str:
    """Presentation-only unit conversion of a raw altitude value (meters)
    already exposed by the domain. This never touches how the domain
    stores or reasons about position — it only decides how the GUI
    displays a number it already has."""
    if units == "imperial":
        miles = altitude_m / 1609.344
        return f"{miles:.1f} mi"
    return f"{altitude_m / 1000:.1f} km"


class FireMissionWindow(QMainWindow):
    """GUI client for a running Forest Fire Mission Simulation.

    This window NEVER decides simulation behaviour. It only calls:
        simulation.start() / .pause() / .resume() / .stop() / .step()
        simulation.world.add_entity() / .remove_entity()
    and renders whatever SimulationSnapshot comes back. All fire
    spreading, detection and alert logic lives in the domain layer — this
    window just constructs plain Satellite/Fire domain objects (the same
    way Scenario.create_world() already does) and hands them to the
    domain's own World, which decides nothing differently because they
    arrived from a button click instead of a scenario script.
    """

    fire_mission_closed = Signal()

    def __init__(self, simulation, settings, parent=None):
        super().__init__(parent)
        self.simulation = simulation
        self.settings = settings
        self._last_snapshot = None
        self._logged_alert_messages = set()
        self._custom_satellite_counter = 0

        self._timer = QTimer(self)
        self._timer.setInterval(self._compute_interval())
        self._timer.timeout.connect(self._advance_step)

        self._setup_window()
        self._connect_signals()
        self._connect_settings()
        self._sync_controls(Simulationstate.INITIALIZED)
        self._refresh_entities_list()

    # ---- setup ------------------------------------------------------
    def _setup_window(self):
        lang = self.settings.language
        self.setWindowTitle(tr("forest_fire_mission", lang))
        self.resize(1280, 860)

        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(14)

        root.addWidget(self._create_header())

        body = QHBoxLayout()
        body.setContentsMargins(20, 0, 20, 16)
        body.setSpacing(14)
        body.addLayout(self._create_simulation_column(), stretch=3)
        body.addLayout(self._create_sidebar_column(), stretch=1)
        root.addLayout(body, stretch=1)

    def _create_header(self):
        lang = self.settings.language
        header = WindowHeader(tr("forest_fire_mission", lang))

        self.start_button = QPushButton(tr("start", lang))
        self.start_button.setObjectName("PrimaryButton")

        self.pause_button = QPushButton(tr("pause", lang))
        self.pause_button.setObjectName("SecondaryButton")

        self.stop_button = QPushButton(tr("stop", lang))
        self.stop_button.setObjectName("DangerButton")

        for button in (self.start_button, self.pause_button, self.stop_button):
            button.setFixedHeight(30)
            button.setFixedWidth(88)
            header.add_action(button)

        self.back_button = header.back_button
        return header

    def _create_simulation_column(self):
        lang = self.settings.language
        column = QVBoxLayout()
        column.setSpacing(8)

        self.simulation_view_header = SectionHeader(tr("simulation_view", lang))
        column.addWidget(self.simulation_view_header)

        self.map_view = MapView()
        self.map_view.setMinimumHeight(420)
        column.addWidget(self.map_view, stretch=1)

        self.log_panel = Panel(title=tr("mission_log", lang))
        self.log_list = QListWidget()
        self.log_list.setObjectName("MissionLog")
        self.log_panel.add_widget(self.log_list)
        column.addWidget(self.log_panel, stretch=1)

        return column

    def _create_sidebar_column(self):
        lang = self.settings.language
        column = QVBoxLayout()
        column.setSpacing(14)

        self.status_panel = Panel(title=tr("mission_status", lang))
        self.time_row = StatusRow(tr("simulation_time", lang), f"0 {tr('steps', lang)}")
        self.state_row = StatusRow(tr("simulation_state", lang), "Initialized")
        self.alerts_row = StatusRow(tr("alerts", lang), "0")
        self.satellites_row = StatusRow(tr("satellites", lang), "0")
        self.fires_row = StatusRow(tr("detected_fires", lang), "0")
        self.altitude_row = StatusRow(tr("altitude", lang), "—")

        for row in (
            self.time_row,
            self.state_row,
            self.alerts_row,
            self.satellites_row,
            self.fires_row,
            self.altitude_row,
        ):
            self.status_panel.add_widget(row)

        column.addWidget(self.status_panel)
        column.addWidget(self._create_entities_panel(), stretch=1)
        return column

    def _create_entities_panel(self):
        lang = self.settings.language
        panel = Panel(title=tr("entities", lang))

        self.entity_type_combo = QComboBox()
        self.entity_type_combo.addItems([tr("satellite_singular", lang), tr("fire_singular", lang)])
        panel.add_widget(self.entity_type_combo)

        coord_row = QHBoxLayout()
        self.lat_input = QDoubleSpinBox()
        self.lat_input.setRange(-90.0, 90.0)
        self.lat_input.setDecimals(4)
        self.lat_input.setValue(DEFAULT_LATITUDE)

        self.lon_input = QDoubleSpinBox()
        self.lon_input.setRange(-180.0, 180.0)
        self.lon_input.setDecimals(4)
        self.lon_input.setValue(DEFAULT_LONGITUDE)

        lat_label = QLabel(tr("latitude", lang))
        lat_label.setObjectName("StatusLabel")
        lon_label = QLabel(tr("longitude", lang))
        lon_label.setObjectName("StatusLabel")

        coord_row.addWidget(lat_label)
        coord_row.addWidget(self.lat_input)
        coord_row.addWidget(lon_label)
        coord_row.addWidget(self.lon_input)
        panel.add_layout(coord_row)

        self.entity_form_stack = QStackedWidget()
        self.entity_form_stack.addWidget(self._create_satellite_form(lang))
        self.entity_form_stack.addWidget(self._create_fire_form(lang))
        panel.add_widget(self.entity_form_stack)

        self.entity_type_combo.currentIndexChanged.connect(
            self.entity_form_stack.setCurrentIndex
        )

        self.add_entity_button = QPushButton(tr("add_entity", lang))
        self.add_entity_button.setObjectName("SecondaryButton")
        panel.add_widget(self.add_entity_button)

        self.entities_list = QListWidget()
        self.entities_list.setObjectName("EntitiesList")
        panel.add_widget(self.entities_list)

        self.remove_entity_button = QPushButton(tr("remove_selected", lang))
        self.remove_entity_button.setObjectName("DangerButton")
        panel.add_widget(self.remove_entity_button)

        self.add_entity_button.clicked.connect(self._on_add_entity)
        self.remove_entity_button.clicked.connect(self._on_remove_selected)

        return panel

    def _create_satellite_form(self, lang) -> QWidget:
        page = QWidget()
        form = QFormLayout(page)
        form.setContentsMargins(0, 4, 0, 4)

        self.mission_name_input = QLineEdit()
        self.mission_name_input.setPlaceholderText(f"Custom-{self._custom_satellite_counter + 1}")

        self.altitude_input = QDoubleSpinBox()
        self.altitude_input.setRange(0, 10_000_000)
        self.altitude_input.setValue(DEFAULT_SATELLITE_ALTITUDE)
        self.altitude_input.setSingleStep(1000)

        self.fov_input = QDoubleSpinBox()
        self.fov_input.setRange(1.0, 180.0)
        self.fov_input.setValue(DEFAULT_SENSOR_FOV)

        self.lat_speed_input = QDoubleSpinBox()
        self.lat_speed_input.setRange(-1.0, 1.0)
        self.lat_speed_input.setDecimals(6)
        self.lat_speed_input.setSingleStep(0.0001)
        self.lat_speed_input.setValue(DEFAULT_LAT_SPEED)

        self.lon_speed_input = QDoubleSpinBox()
        self.lon_speed_input.setRange(-1.0, 1.0)
        self.lon_speed_input.setDecimals(6)
        self.lon_speed_input.setSingleStep(0.0001)
        self.lon_speed_input.setValue(DEFAULT_LON_SPEED)

        form.addRow(tr("mission_name", lang), self.mission_name_input)
        form.addRow(tr("altitude_field", lang), self.altitude_input)
        form.addRow(tr("sensor_fov", lang), self.fov_input)
        form.addRow(tr("lat_speed", lang), self.lat_speed_input)
        form.addRow(tr("lon_speed", lang), self.lon_speed_input)

        return page

    def _create_fire_form(self, lang) -> QWidget:
        page = QWidget()
        form = QFormLayout(page)
        form.setContentsMargins(0, 4, 0, 4)

        self.intensity_input = QDoubleSpinBox()
        self.intensity_input.setRange(0.0, 1.0)
        self.intensity_input.setSingleStep(0.05)
        self.intensity_input.setValue(DEFAULT_FIRE_INTENSITY)

        self.radius_input = QDoubleSpinBox()
        self.radius_input.setRange(0, 100_000)
        self.radius_input.setValue(DEFAULT_FIRE_RADIUS)

        self.spread_rate_input = QDoubleSpinBox()
        self.spread_rate_input.setRange(0, 1000)
        self.spread_rate_input.setValue(DEFAULT_FIRE_SPREAD_RATE)

        form.addRow(tr("intensity", lang), self.intensity_input)
        form.addRow(tr("radius", lang), self.radius_input)
        form.addRow(tr("spread_rate", lang), self.spread_rate_input)

        return page

    def _connect_signals(self):
        self.back_button.clicked.connect(self.close)
        self.start_button.clicked.connect(self._on_start_clicked)
        self.pause_button.clicked.connect(self._on_pause_clicked)
        self.stop_button.clicked.connect(self._on_stop_clicked)

    def _connect_settings(self):
        self.settings.simulation_speed_changed.connect(self._on_speed_changed)
        self.settings.units_changed.connect(lambda _: self._refresh_altitude())

    # ---- simulation control ------------------------------------------
    def _compute_interval(self) -> int:
        speed = max(self.settings.simulation_speed, 0.05)
        return max(MIN_STEP_INTERVAL_MS, int(BASE_STEP_INTERVAL_MS / speed))

    def _on_speed_changed(self, _speed: float):
        self._timer.setInterval(self._compute_interval())

    def _on_start_clicked(self):
        lang = self.settings.language
        if self.simulation.current_state == Simulationstate.PAUSED:
            self.simulation.resume()
            self._log(f"{tr('resume', lang)}.")
        else:
            self.simulation.start()
            self._log(f"{tr('start', lang)}.")

        self._timer.start()
        self._sync_controls(self.simulation.current_state)

    def _on_pause_clicked(self):
        self.simulation.pause()
        self._timer.stop()
        self._sync_controls(self.simulation.current_state)
        self._log(f"{tr('pause', self.settings.language)}.")

    def _on_stop_clicked(self):
        self.simulation.stop()
        self._timer.stop()
        self._sync_controls(self.simulation.current_state)
        self._log(f"{tr('stop', self.settings.language)}.")

    def _advance_step(self):
        snapshot = self.simulation.step()
        if snapshot is not None:
            self._render_snapshot(snapshot)

    # ---- rendering ------------------------------------------------------
    def _render_snapshot(self, snapshot):
        self._last_snapshot = snapshot
        lang = self.settings.language

        self.map_view.update_snapshot(snapshot)

        self.time_row.set_value(f"{snapshot.step} {tr('steps', lang)}")
        self.state_row.set_value(self._state_label(snapshot.simulation_state))
        self.alerts_row.set_value(len(snapshot.alerts))
        self.satellites_row.set_value(len(snapshot.satellite))
        self.fires_row.set_value(len(snapshot.fire))
        self._refresh_altitude()
        self._refresh_entities_list()

        # Only append an alert to the Mission Log the first time its exact
        # message is seen. The domain still returns the full alert list on
        # every single step (that's its own, unchanged behaviour) — this
        # dedup is a GUI-only decision about what's worth showing the user,
        # so a still-burning fire doesn't reprint the same line forever.
        for alert in snapshot.alerts:
            message = str(alert)
            if message not in self._logged_alert_messages:
                self._logged_alert_messages.add(message)
                self._log(message)

    def _refresh_altitude(self):
        if self._last_snapshot and self._last_snapshot.satellite:
            altitude_m = self._last_snapshot.satellite[0].position.altitude
            self.altitude_row.set_value(format_altitude(altitude_m, self.settings.units))
        else:
            self.altitude_row.set_value("—")

    def _sync_controls(self, state):
        is_running = state == Simulationstate.RUNNING
        is_paused = state == Simulationstate.PAUSED
        is_stopped = state == Simulationstate.STOPPED
        lang = self.settings.language

        self.start_button.setEnabled(not is_running and not is_stopped)
        self.start_button.setText(tr("resume", lang) if is_paused else tr("start", lang))
        self.pause_button.setEnabled(is_running)
        self.stop_button.setEnabled(is_running or is_paused)

        self.state_row.set_value(self._state_label(state))

    @staticmethod
    def _state_label(state) -> str:
        return state.value if hasattr(state, "value") else str(state)

    def _log(self, message: str):
        self.log_list.addItem(message)
        self.log_list.scrollToBottom()

    # ---- entity management ----------------------------------------------
    def _on_add_entity(self):
        if self.entity_type_combo.currentIndex() == 0:
            self._add_satellite_from_form()
        else:
            self._add_fire_from_form()

    def _add_satellite_from_form(self):
        position = Position(
            latitude=self.lat_input.value(),
            longitude=self.lon_input.value(),
            altitude=self.altitude_input.value(),
        )
        sensor = Sensor(field_of_view=self.fov_input.value())

        self._custom_satellite_counter += 1
        name = self.mission_name_input.text().strip() or f"Custom-{self._custom_satellite_counter}"

        satellite = Satellite(
            mission_name=name,
            position=position,
            sensor=sensor,
            angular_speed=(self.lat_speed_input.value(), self.lon_speed_input.value(), 0),
        )
        self.simulation.world.add_entity(satellite)
        self._log(f"+ {satellite}")
        self._refresh_entities_list()

        self.mission_name_input.clear()
        self.mission_name_input.setPlaceholderText(f"Custom-{self._custom_satellite_counter + 1}")

    def _add_fire_from_form(self):
        position = Position(
            latitude=self.lat_input.value(),
            longitude=self.lon_input.value(),
            altitude=0,
        )
        fire = Fire(
            position=position,
            intensity=self.intensity_input.value(),
            radius=self.radius_input.value(),
            spread_rate=self.spread_rate_input.value(),
        )
        self.simulation.world.add_entity(fire)
        self._log(f"+ {fire}")
        self._refresh_entities_list()

    def _on_remove_selected(self):
        item = self.entities_list.currentItem()
        if item is None:
            return

        entity = item.data(Qt.UserRole)
        self.simulation.world.remove_entity(entity)
        self._log(f"- {entity}")
        self._refresh_entities_list()

    def _refresh_entities_list(self):
        selected_entity = None
        current_item = self.entities_list.currentItem()
        if current_item is not None:
            selected_entity = current_item.data(Qt.UserRole)

        self.entities_list.clear()
        selected_row = -1

        for index, entity in enumerate(self.simulation.world.entities):
            item = QListWidgetItem(str(entity))
            item.setData(Qt.UserRole, entity)
            self.entities_list.addItem(item)
            if entity is selected_entity:
                selected_row = index

        if selected_row >= 0:
            self.entities_list.setCurrentRow(selected_row)

    # ---- lifecycle --------------------------------------------------
    def closeEvent(self, event):
        self._timer.stop()
        self.fire_mission_closed.emit()
        super().closeEvent(event)
