from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel

from gui.components.back_button import BackButton


class WindowHeader(QWidget):
    """Consistent top bar shared by every secondary window (Fire Mission,
    Settings, About): a Back control on the left, the window title next to
    it, and an optional right-hand area for window-specific actions (e.g.
    FireMissionWindow's Start/Pause/Stop controls).

    This replaces near-identical `_create_header()` code that used to be
    copy-pasted across three windows with a single shared implementation.
    """

    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setObjectName("WindowHeader")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(14)

        self.back_button = BackButton()
        layout.addWidget(self.back_button)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("WindowTitle")
        layout.addWidget(self.title_label)

        layout.addStretch()

        self._actions_layout = QHBoxLayout()
        self._actions_layout.setSpacing(8)
        layout.addLayout(self._actions_layout)

    def add_action(self, widget: QWidget) -> None:
        """Add a widget (e.g. a button) to the right-hand action area."""
        self._actions_layout.addWidget(widget)
