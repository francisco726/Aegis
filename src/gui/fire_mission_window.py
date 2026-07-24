from PySide6.QtCore import Signal, QTimer
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QListWidget,
)

from gui.components.window_header import WindowHeader
from gui.components.panel import Panel
from gui.components.status_row import StatusRow
from gui.components.section_header import SectionHeader
from gui.components.map_view import MapView

from domain.simulation_state import Simulationstate


class FireMissionWindow(QMainWindow):
    """GUI client for a running Forest Fire Mission Simulation.

    This window NEVER decides simulation behaviour. It only calls:
        simulation.start() / .pause() / .resume() / .stop() / .step()
    and renders whatever SimulationSnapshot comes back from .step(). All
    fire spreading, detection and alert logic lives in the domain layer;
    this window does not know (and must not need to know) how any of it
    works internally.
    """

    fire_mission_closed = Signal()

    STEP_INTERVAL_MS = 800

    def __init__(self, simulation, parent=None):
        super().__init__(parent)
        self.simulation = simulation

        self._timer = QTimer(self)
        self._timer.setInterval(self.STEP_INTERVAL_MS)
        self._timer.timeout.connect(self._advance_step)

        self._setup_window()
        self._connect_signals()
        self._sync_controls(Simulationstate.INITIALIZED)

    # ---- setup ------------------------------------------------------
    def _setup_window(self):
        self.setWindowTitle("Forest Fire Mission")
        self.resize(1280, 820)

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
        header = WindowHeader("Forest Fire Mission")

        self.start_button = QPushButton("Start")
        self.start_button.setObjectName("PrimaryButton")

        self.pause_button = QPushButton("Pause")
        self.pause_button.setObjectName("SecondaryButton")

        self.stop_button = QPushButton("Stop")
        self.stop_button.setObjectName("DangerButton")

        for button in (self.start_button, self.pause_button, self.stop_button):
            button.setFixedHeight(32)
            button.setFixedWidth(90)
            header.add_action(button)

        self.back_button = header.back_button
        return header

    def _create_simulation_column(self):
        column = QVBoxLayout()
        column.setSpacing(8)
        column.addWidget(SectionHeader("Simulation View"))

        self.map_view = MapView()
        self.map_view.setMinimumHeight(420)
        column.addWidget(self.map_view, stretch=1)

        self.log_panel = Panel(title="Mission Log")
        self.log_list = QListWidget()
        self.log_list.setObjectName("MissionLog")
        self.log_panel.add_widget(self.log_list)
        column.addWidget(self.log_panel, stretch=1)

        return column

    def _create_sidebar_column(self):
        column = QVBoxLayout()

        self.status_panel = Panel(title="Mission Status")
        self.time_row = StatusRow("Simulation Time", "0 steps")
        self.state_row = StatusRow("Simulation State", "Initialized")
        self.alerts_row = StatusRow("Alerts", "0")
        self.satellites_row = StatusRow("Satellites", "0")
        self.fires_row = StatusRow("Detected Fires", "0")

        for row in (
            self.time_row,
            self.state_row,
            self.alerts_row,
            self.satellites_row,
            self.fires_row,
        ):
            self.status_panel.add_widget(row)

        column.addWidget(self.status_panel)
        column.addStretch()
        return column

    def _connect_signals(self):
        self.back_button.clicked.connect(self.close)
        self.start_button.clicked.connect(self._on_start_clicked)
        self.pause_button.clicked.connect(self._on_pause_clicked)
        self.stop_button.clicked.connect(self._on_stop_clicked)

    # ---- simulation control ------------------------------------------
    def _on_start_clicked(self):
        if self.simulation.current_state == Simulationstate.PAUSED:
            self.simulation.resume()
            self._log("Simulation resumed.")
        else:
            self.simulation.start()
            self._log("Simulation started.")

        self._timer.start()
        self._sync_controls(self.simulation.current_state)

    def _on_pause_clicked(self):
        self.simulation.pause()
        self._timer.stop()
        self._sync_controls(self.simulation.current_state)
        self._log("Simulation paused.")

    def _on_stop_clicked(self):
        self.simulation.stop()
        self._timer.stop()
        self._sync_controls(self.simulation.current_state)
        self._log("Simulation stopped.")

    def _advance_step(self):
        snapshot = self.simulation.step()
        if snapshot is not None:
            self._render_snapshot(snapshot)

    # ---- rendering ------------------------------------------------------
    def _render_snapshot(self, snapshot):
        self.map_view.update_snapshot(snapshot)

        self.time_row.set_value(f"{snapshot.step} steps")
        self.state_row.set_value(self._state_label(snapshot.simulation_state))
        self.alerts_row.set_value(len(snapshot.alerts))
        self.satellites_row.set_value(len(snapshot.satellite))
        self.fires_row.set_value(len(snapshot.fire))

        for alert in snapshot.alerts:
            self._log(str(alert))

    def _sync_controls(self, state):
        is_running = state == Simulationstate.RUNNING
        is_paused = state == Simulationstate.PAUSED
        is_stopped = state == Simulationstate.STOPPED

        self.start_button.setEnabled(not is_running and not is_stopped)
        self.start_button.setText("Resume" if is_paused else "Start")
        self.pause_button.setEnabled(is_running)
        self.stop_button.setEnabled(is_running or is_paused)

        self.state_row.set_value(self._state_label(state))

    @staticmethod
    def _state_label(state) -> str:
        return state.value if hasattr(state, "value") else str(state)

    def _log(self, message: str):
        self.log_list.addItem(message)
        self.log_list.scrollToBottom()

    # ---- lifecycle --------------------------------------------------
    def closeEvent(self, event):
        self._timer.stop()
        self.fire_mission_closed.emit()
        super().closeEvent(event)
