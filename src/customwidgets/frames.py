"""custom QFrame classes"""

from PyQt6.QtWidgets import QFrame, QHBoxLayout
from .labels import Label


class Line(QFrame):

    def __init__(self, horizontal=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if horizontal:
            # defaults to horizontal line
            self.setFrameShape(QFrame.Shape.HLine)
        else:
            self.setFrameShape(QFrame.Shape.VLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)


class ItemDisplay(QFrame):
    """bill item for displaying details"""

    def __init__(self, name: str, value: float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFrameStyle(QFrame.Shape.WinPanel | QFrame.Shadow.Raised)

        mlayout = QHBoxLayout(self)

        self.name = Label(f"<strong>{name}</strong>")

        self.value = Label(f"{value:,.2f}")

        mlayout.addWidget(self.name, stretch=1)
        mlayout.addWidget(Line(horizontal=False))
        mlayout.addWidget(self.value, stretch=6)
