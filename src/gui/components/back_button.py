from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt


class BackButton(QPushButton):
    """Text-based back-navigation control ("← Back").

    Replaces the earlier circular icon button: a flat, minimal-chrome text
    button reads as professional desktop software (Qt Creator, VS Code,
    QGroundControl) rather than a mobile-app affordance, and it drops the
    dependency on an external icon asset entirely.
    """

    def __init__(self, text: str = "Back", parent=None):
        super().__init__(f"\u2190  {text}", parent)
        self.setObjectName("BackButton")
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(30)
