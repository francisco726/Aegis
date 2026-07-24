from PySide6.QtWidgets import QLabel


class SectionHeader(QLabel):
    """Small uppercase label used to title a section of a window
    (e.g. "MISSION", "GENERAL", "SIMULATION VIEW")."""

    def __init__(self, text: str, parent=None):
        super().__init__(text.upper(), parent)
        self.setObjectName("SectionHeader")
