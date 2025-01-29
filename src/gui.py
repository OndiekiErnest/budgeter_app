"""gui of the budgeter app"""

from PyQt6.QtWidgets import (
    QWidget,
    QStackedWidget,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from customwidgets import (
    NamedLineedit,
    Button,
    ItemsArea,
    SettingsGUI,
    NamedLabel,
    NewExpenseDialog,
)
from utils import app_settings
from constants import Expense, BACK_ICON, ADD_ICON, SETTINGS_ICON, EQUAL_ICON, APP_ICON


class BudgeterSettings(QWidget):
    """expense settings screen"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        mlayout = QVBoxLayout(self)
        mlayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        btnslayout = QHBoxLayout()

        self.back_btn = Button()
        self.back_btn.setIcon(QIcon(BACK_ICON))

        self.add_expense_btn = Button()
        self.add_expense_btn.setIcon(QIcon(ADD_ICON))
        self.add_expense_btn.clicked.connect(self.on_new_expense)

        self.expense_settings = SettingsGUI()

        self.new_expense_popup = NewExpenseDialog(
            Expense(name="", description=""), self
        )

        btnslayout.addWidget(self.back_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        btnslayout.addWidget(
            self.add_expense_btn, alignment=Qt.AlignmentFlag.AlignRight
        )

        mlayout.addLayout(btnslayout)
        mlayout.addWidget(self.expense_settings)

    def on_new_expense(self):
        """when adding new expense"""
        if self.new_expense_popup.exec():
            app_settings["expenses"].insert(
                0,
                self.new_expense_popup.get_expense(),
            )
            self.expense_settings.refresh()


class BudgeterIO(QWidget):
    """budgeter input/output screen"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Budgeter")

        mlayout = QVBoxLayout(self)
        mlayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        btnslayout = QHBoxLayout()
        btnslayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.tt_amt_input = NamedLineedit("Amount")
        self.tt_amt_input.child.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.settings_btn = Button("Expenses")
        self.settings_btn.setIcon(QIcon(SETTINGS_ICON))

        self.calc_bills_btn = Button("Calculate")
        self.calc_bills_btn.setIcon(QIcon(EQUAL_ICON))

        self.message_label = NamedLabel(
            "Get started",
            "Set your expenses in the settings then enter your budget amount to calculate",
        )

        self.items_area = ItemsArea()
        self.items_area.hide()

        btnslayout.addWidget(self.calc_bills_btn)
        btnslayout.addWidget(self.settings_btn)

        mlayout.addWidget(self.tt_amt_input)
        mlayout.addLayout(btnslayout)
        mlayout.addWidget(self.items_area)
        mlayout.addWidget(self.message_label, alignment=Qt.AlignmentFlag.AlignHCenter)

    def create_fields(
        self,
        fields: list[Expense],
        fixed_total: float,
        variable_total: float,
    ):
        """create fields"""
        self.items_area.add_items(fields, fixed_total, variable_total)
        self.items_area.show()
        self.message_label.hide()

    def show_message(self, title: str, message: str):
        self.items_area.hide()
        self.message_label.setTitle(title)
        self.message_label.child.setText(message)
        self.message_label.show()


class BudgeterGUI(QWidget):
    """budgeter app GUI"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Budgeter")
        self.setWindowIcon(QIcon(APP_ICON))

        mlayout = QVBoxLayout(self)
        mlayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        mlayout.setContentsMargins(0, 0, 0, 0)

        self.widgets_stack = QStackedWidget()
        mlayout.addWidget(self.widgets_stack)

        self.budgeter_io = BudgeterIO()
        self.expense_setts = BudgeterSettings()

        self.budgeter_io.settings_btn.clicked.connect(
            lambda: self.switch_to_widget(self.expense_setts)
        )
        self.expense_setts.back_btn.clicked.connect(
            lambda: self.switch_to_widget(self.budgeter_io),
        )

        self.widgets_stack.addWidget(self.budgeter_io)
        self.widgets_stack.addWidget(self.expense_setts)

    def switch_to_widget(self, widget: QWidget):
        self.widgets_stack.setCurrentWidget(widget)
