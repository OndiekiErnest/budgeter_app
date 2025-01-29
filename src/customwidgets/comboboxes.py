"""custom QComboBox classes"""

from PyQt6.QtWidgets import QComboBox, QGroupBox, QVBoxLayout


class Combobox(QComboBox):
    """custom QComboBox"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NamedCombobox(QGroupBox):
    """QComboBox in a QGroupBox"""

    def __init__(self, title: str, *args, **kwargs):
        super().__init__(title)

        mlayout = QVBoxLayout(self)

        self.child = Combobox(*args, **kwargs)

        mlayout.addWidget(self.child)

    def text(self):
        return self.child.currentText()

    def setText(self, text: str):
        self.child.setCurrentText(text)

    def clear(self):
        self.child.setCurrentIndex(0)
