from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel


class StatusRow(QWidget):
    """A single "Label ... Value" row, used inside status/info panels
    (Mission Status, About, Settings). `set_value()` lets the parent window
    refresh it cheaply every simulation step without rebuilding layout."""

    def __init__(self, label: str, value="—", parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 2, 0, 2)

        self.label = QLabel(label)
        self.label.setObjectName("StatusLabel")

        self.value_label = QLabel(str(value))
        self.value_label.setObjectName("StatusValue")
        self.value_label.setWordWrap(True)

        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(self.value_label)

    def set_value(self, value) -> None:
        self.value_label.setText(str(value))
