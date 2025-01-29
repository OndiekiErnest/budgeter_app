"""custom QPushButton classes"""

from PyQt6.QtWidgets import QPushButton, QGroupBox, QVBoxLayout


class Button(QPushButton):
    """custom QPushButton"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # set the minimum size
        self.setMinimumSize(70, 30)
        self.setMaximumSize(120, 50)


class NamedButton(QGroupBox):
    """QPushButton in a QGroupBox"""

    def __init__(self, title: str, *args, **kwargs):
        super().__init__(title)

        layout = QVBoxLayout(self)
        self.child = Button(*args, **kwargs)

        layout.addWidget(self.child)

    def text(self):
        return self.child.text()

    def setText(self, text: str):
        self.child.setText(text)
