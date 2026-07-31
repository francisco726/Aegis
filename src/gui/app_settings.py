from PySide6.QtCore import QObject, Signal


class AppSettings(QObject):
    """Single source of truth for user-facing application preferences.

    Theme, language, playback speed and display units are GUI/application
    concerns, not domain concerns — the domain has no notion of any of
    this, and none of it is stored here in a way that reaches into
    domain objects. One instance is created in main.py and threaded
    through every window that needs to read or react to a preference, so
    there is exactly one place these values live and one signal per
    preference for windows to react to changes live.
    """

    theme_changed = Signal(str)                 # "dark" | "light"
    language_changed = Signal(str)               # "en" | "pt"
    simulation_speed_changed = Signal(float)      # multiplier, e.g. 0.2 .. 2.0
    units_changed = Signal(str)                  # "metric" | "imperial"

    def __init__(self):
        super().__init__()
        self._theme = "dark"
        self._language = "en"
        self._simulation_speed = 1.0
        self._units = "metric"

    # ---- theme --------------------------------------------------------
    @property
    def theme(self) -> str:
        return self._theme

    def set_theme(self, value: str) -> None:
        if value != self._theme:
            self._theme = value
            self.theme_changed.emit(value)

    # ---- language -----------------------------------------------------
    @property
    def language(self) -> str:
        return self._language

    def set_language(self, value: str) -> None:
        if value != self._language:
            self._language = value
            self.language_changed.emit(value)

    # ---- simulation speed ----------------------------------------------
    @property
    def simulation_speed(self) -> float:
        return self._simulation_speed

    def set_simulation_speed(self, value: float) -> None:
        if value != self._simulation_speed:
            self._simulation_speed = value
            self.simulation_speed_changed.emit(value)

    # ---- units ----------------------------------------------------------
    @property
    def units(self) -> str:
        return self._units

    def set_units(self, value: str) -> None:
        if value != self._units:
            self._units = value
            self.units_changed.emit(value)
