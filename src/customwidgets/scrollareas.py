from PyQt6.QtWidgets import QWidget, QScrollArea, QGroupBox, QVBoxLayout
from PyQt6.QtCore import Qt

from .frames import ItemDisplay
from .settings import ExpenseWidget
from .comboboxes import NamedCombobox

from constants import Expense, Category, Comma
from utils import delete_widgets, app_settings


def skey(item: Expense):
    return item.amount, len(item.name)


class ItemsArea(QScrollArea):
    """scrollable area with 2 sections: fixed and variable"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.setWidgetResizable(True)

        main_widget = QWidget()
        main_widget.setFixedWidth(900)

        self.setWidget(main_widget)
        mlayout = QVBoxLayout(main_widget)
        mlayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        mlayout.setSpacing(30)

        self.fixed_group = QGroupBox("Fixed Expenses")
        self.variable_group = QGroupBox("Variable Expenses")
        mlayout.addWidget(self.fixed_group)
        mlayout.addWidget(self.variable_group)

        self.fixed_group_layout = QVBoxLayout(self.fixed_group)
        self.variable_group_layout = QVBoxLayout(self.variable_group)

    def add_items(
        self, items: list[Expense], fixed_total: float, variable_total: float
    ):
        """add bill items to groups"""
        delete_widgets(self.fixed_group_layout)
        delete_widgets(self.variable_group_layout)

        self.fixed_group.setTitle(f"Fixed Expenses ({fixed_total:,.2f})")
        self.variable_group.setTitle(f"Variable Expenses ({variable_total:,.2f})")

        for field in sorted(items, key=skey, reverse=True):

            f_upper = field.name.upper()
            setattr(
                self,
                f_upper,
                ItemDisplay(field.name.title(), field.amount),
            )

            if item_widget := getattr(self, f_upper, None):
                item_widget.setToolTip(field.description)

                if field.category == Category.FIXED:
                    self.fixed_group_layout.addWidget(item_widget)
                elif field.category == Category.VARIABLE:
                    self.variable_group_layout.addWidget(item_widget)


class SettingsGUI(QScrollArea):
    """settings screen"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.setWidgetResizable(True)

        main_widget = QWidget()
        main_widget.setFixedWidth(900)

        self.setWidget(main_widget)
        mlayout = QVBoxLayout(main_widget)
        mlayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        mlayout.setSpacing(30)

        fixed_group = QGroupBox("Fixed Expenses")
        variable_group = QGroupBox("Variable Expenses")
        other_group = QGroupBox("Other Settings")

        mlayout.addWidget(fixed_group)
        mlayout.addWidget(variable_group)
        mlayout.addWidget(other_group)

        self.fixed_group_layout = QVBoxLayout(fixed_group)
        self.variable_group_layout = QVBoxLayout(variable_group)
        self.other_group_layout = QVBoxLayout(other_group)

        self.create_settings()

    def create_settings(self):
        """create settings fields"""

        comma_value = app_settings["comma"]

        comma_widget = NamedCombobox("Parse a comma (,) as a:")
        comma_widget.child.currentTextChanged.connect(self.edit_comma)
        comma_widget.child.addItems(item.value for item in Comma)
        comma_widget.setText(str(comma_value))

        self.other_group_layout.addWidget(comma_widget)

        expenses: list[Expense] = app_settings["expenses"]
        for expense in expenses:
            widget = ExpenseWidget(expense)
            if expense.category == Category.FIXED:
                self.fixed_group_layout.addWidget(widget)
            elif expense.category == Category.VARIABLE:
                self.variable_group_layout.addWidget(widget)

    def edit_comma(self, current: str):
        """update comma when its value changes"""
        app_settings["comma"] = Comma(current)

    def refresh(self):
        """redraw settings"""
        delete_widgets(self.fixed_group_layout)
        delete_widgets(self.variable_group_layout)

        self.create_settings()
