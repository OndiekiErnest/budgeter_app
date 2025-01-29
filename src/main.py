"""main app logic"""

from gui import BudgeterGUI
from utils import parse_amt, app_settings, save_settings
from constants import Category


class MainApp(BudgeterGUI):
    """main app"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.budgeter_io.calc_bills_btn.clicked.connect(self.calculate)
        self.budgeter_io.tt_amt_input.child.returnPressed.connect(self.calculate)

    def calculate(self):
        """get amount and calculate"""
        if (amt := parse_amt(self.budgeter_io.tt_amt_input.child.text())) is not None:

            variable_items = (
                item
                for item in app_settings["expenses"]
                if item.category == Category.VARIABLE
            )

            fixed_total = sum(
                item.amount
                for item in app_settings["expenses"]
                if item.category == Category.FIXED
            )
            if fixed_total > amt:
                self.budgeter_io.show_message(
                    "Failed to calculate",
                    f"The amount you entered is lower than the sum of all fixed expenses ({fixed_total:,.2f})",
                )
                return

            amt -= fixed_total

            for item in variable_items:
                item.amount = item.percentage / 100 * amt

            self.budgeter_io.create_fields(app_settings["expenses"], fixed_total, amt)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet("QWidget{font:18px}")

    main = MainApp()
    main.showMaximized()

    exit_code = app.exec()

    save_settings(app_settings)

    sys.exit(exit_code)
