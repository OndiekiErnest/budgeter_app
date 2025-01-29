"""custom QLabel classes"""

from PyQt6.QtWidgets import QLabel, QGroupBox, QVBoxLayout
from PyQt6.QtCore import Qt


class Label(QLabel):
    """custom QLabel"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
            | Qt.TextInteractionFlag.LinksAccessibleByMouse
            | Qt.TextInteractionFlag.TextSelectableByKeyboard
        )
        # self.setAlignment(Qt.AlignmentFlag.AlignCenter)


class NamedLabel(QGroupBox):
    """QLabel in a QGroupBox"""

    def __init__(self, title: str, *args, **kwargs):
        super().__init__(title)

        layout = QVBoxLayout(self)
        self.child = Label(*args, **kwargs)

        layout.addWidget(self.child)

    def text(self):
        return self.child.text()

    def setText(self, text: str):
        self.child.setText(text)

    def clear(self):
        self.child.clear()
