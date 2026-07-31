from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel


class StatusBar(QWidget):
    """A slim, full-width, solid-accent-colored status strip along the
    bottom of a window — the same convention VS Code and JetBrains IDEs
    use for their bottom bar. A flat accent-filled strip like this is one
    of the more recognizable "real IDE" signals, so it's worth having
    even though (for now) it just shows static text.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("StatusBar")
        self.setFixedHeight(24)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)

        self.label = QLabel("")
        self.label.setObjectName("StatusBarLabel")
        layout.addWidget(self.label)
        layout.addStretch()

    def set_text(self, text: str) -> None:
        self.label.setText(text)
