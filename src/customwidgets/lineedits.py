"""custom QLineEdit classes"""

from PyQt6.QtWidgets import QLineEdit, QGroupBox, QVBoxLayout


class Lineedit(QLineEdit):
    """custom QLineEdit"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumHeight(30)


class NamedLineedit(QGroupBox):
    """QLineEdit in a QGroupBox"""

    def __init__(self, title: str, *args, **kwargs):
        super().__init__(title)

        layout = QVBoxLayout(self)
        self.child = Lineedit(*args, **kwargs)

        layout.addWidget(self.child)

    def text(self):
        return self.child.text()

    def setText(self, text: str):
        self.child.setText(text)

    def clear(self):
        self.child.clear()
