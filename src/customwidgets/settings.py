"""settings custom widgets"""

from PyQt6.QtWidgets import (
    QFrame,
    QDialog,
    QDialogButtonBox,
    QMessageBox,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
)
from PyQt6.QtGui import QRegularExpressionValidator, QIcon
from PyQt6.QtCore import Qt, QRegularExpression
from .lineedits import NamedLineedit
from .buttons import Button
from .frames import Line
from .comboboxes import NamedCombobox

from constants import Category, Comma, Expense, SettingValue, UPDATE_ICON, DELETE_ICON
from utils import delete_widgets, app_settings


class BaseExpenseWidget(QFrame):
    """base class: editable, deletable expense QFrame widget"""

    __slots__ = ("mlayout", "itemslayout", "key_metadata", "expense")

    def __init__(self, expense: Expense, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)
        self.setMinimumHeight(330)

        self.mlayout = QVBoxLayout(self)
        self.mlayout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        self.itemslayout = QGridLayout()
        self.mlayout.addLayout(self.itemslayout)

        self.key_metadata: dict[str, SettingValue] = {}

        self.display(expense)

    def display(self, expense: Expense):
        """display the specified expense"""
        self.expense = expense

        col = 0
        row = 0
        for k, v in expense.items():
            # print(k, repr(v))

            if isinstance(v, Category):
                values = [item.value for item in Category]
                widget = NamedCombobox(k.title())
                widget.child.addItems(values)
                widget.setText(str(v))
                self.key_metadata[k] = SettingValue(widget=widget, caster=Category)

            elif isinstance(v, Comma):
                values = [item.value for item in Comma]
                widget = NamedCombobox(k.title())
                widget.child.addItems(values)
                widget.setText(str(v))
                self.key_metadata[k] = SettingValue(widget=widget, caster=Comma)

            elif isinstance(v, str):
                widget = NamedLineedit(k.title(), v)
                self.key_metadata[k] = SettingValue(widget=widget)

            elif isinstance(v, (float, int)):
                # create custom validator for this widget
                reg_ex = QRegularExpression(r"[0-9]+[.]*")
                validator = QRegularExpressionValidator(reg_ex)

                widget = NamedLineedit(k.title())
                widget.child.setValidator(validator)
                widget.setText(str(v))
                self.key_metadata[k] = SettingValue(widget=widget, caster=float)

            else:  # assume they support str, and its caster is type(v)
                widget = NamedLineedit(k.title(), str(v))
                self.key_metadata[k] = SettingValue(widget=widget, caster=type(v))

            if row == 2:
                self.itemslayout.addWidget(widget, row, col, 1, -1)
            else:
                self.itemslayout.addWidget(widget, row, col)

            col += 1
            if col > 1:
                col = 0
                row += 1

        self.mlayout.addWidget(Line())

    def clear(self, key: str):
        self.key_metadata[key].widget.clear()

    def can_continue(self):
        return (
            QMessageBox.question(
                self,
                "Confirm Delete",
                f"Delete '{self.expense.name}' Expense\nAre you sure you want to continue?",
            )
            == QMessageBox.StandardButton.Yes
        )


class ExpenseWidget(BaseExpenseWidget):
    """editable, deletable expense QFrame widget"""

    __slots__ = ("edit_btn", "delete_btn")

    def __init__(self, expense: Expense, *args, **kwargs):
        super().__init__(expense, *args, **kwargs)

    def display(self, expense: Expense):
        """display the specified expense"""
        super().display(expense)

        btnslayout = QHBoxLayout()
        btnslayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.edit_btn = Button()
        self.edit_btn.setIcon(QIcon(UPDATE_ICON))
        self.edit_btn.clicked.connect(self.edit_expense)
        self.edit_btn.hide()

        self.delete_btn = Button()
        self.delete_btn.setIcon(QIcon(DELETE_ICON))
        self.delete_btn.clicked.connect(self.delete_this)
        self.delete_btn.hide()

        btnslayout.addWidget(self.edit_btn)
        btnslayout.addWidget(self.delete_btn)

        self.mlayout.addLayout(btnslayout)

    def _show_btns(self):
        """show btns"""
        self.edit_btn.show()
        self.delete_btn.show()

    def _hide_btns(self):
        """hide btns"""
        self.edit_btn.hide()
        self.delete_btn.hide()

    def _clear_widgets(self):
        """delete widgets"""
        self.edit_btn.clicked.disconnect(self.edit_expense)
        self.delete_btn.clicked.disconnect(self.delete_this)

        self.key_metadata.clear()

        delete_widgets(self.mlayout)

    def delete_this(self):
        """delete this widget"""
        if self.can_continue():
            self._clear_widgets()
            self.deleteLater()

            expenses: list[Expense] = app_settings["expenses"]
            expenses.remove(self.expense)

    def edit_expense(self):
        """save edits of the expense"""
        if self.expense:
            for k, sett in self.key_metadata.items():

                setattr(self.expense, k, sett.value())

    def enterEvent(self, event):
        self._show_btns()

    def leaveEvent(self, a0):
        self._hide_btns()


class NewExpenseDialog(QDialog):
    """popup widget to add new expense"""

    __slots__ = ()

    def __init__(self, expense: Expense, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Add New Expense")

        mlayout = QVBoxLayout(self)

        self.expense_widget = BaseExpenseWidget(expense)

        dialog_btns = (
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttonBox = QDialogButtonBox(dialog_btns)
        buttonBox.accepted.connect(self.okay_clicked)
        buttonBox.rejected.connect(self.reject)

        mlayout.addWidget(self.expense_widget)
        mlayout.addWidget(buttonBox, alignment=Qt.AlignmentFlag.AlignRight)

    def get_expense(self):
        """return an Expense object"""
        data = {k: v.value() for k, v in self.expense_widget.key_metadata.items()}
        exp = Expense(**data)
        self.expense_widget.clear("name")

        return exp

    def isvalid_entry(self):
        """is a valid entry"""
        data = {k: v.value() for k, v in self.expense_widget.key_metadata.items()}

        percentage = data.pop("percentage")
        amount = data.pop("amount")

        return all(v for _, v in data.items()) and (percentage or amount)

    def okay_clicked(self):
        """save edits of the expense"""
        if self.isvalid_entry():
            self.accept()
