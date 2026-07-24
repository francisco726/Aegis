from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel


class Panel(QFrame):
    """A titled, bordered surface ("card") used to group related content.

    Every boxed section across the app — Mission Status, Mission Log,
    the mission-selection card on the Home screen, the Settings groups,
    the About info block — is a Panel. This keeps the visual language
    (background, border, radius, spacing) defined in exactly one place
    (see theme.py, selector `QFrame#Panel`).
    """

    def __init__(self, title: str | None = None, parent=None):
        super().__init__(parent)
        self.setObjectName("Panel")

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(16, 14, 16, 16)
        self._layout.setSpacing(10)

        self.title_label = None
        if title:
            self.title_label = QLabel(title)
            self.title_label.setObjectName("PanelTitle")
            self._layout.addWidget(self.title_label)

    def add_widget(self, widget):
        self._layout.addWidget(widget)

    def add_layout(self, layout):
        self._layout.addLayout(layout)

    def body_layout(self) -> QVBoxLayout:
        return self._layout
