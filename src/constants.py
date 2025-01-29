"""common constants"""

from enum import StrEnum
from dataclasses import dataclass, asdict, fields
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SETTINGS_FILE = os.path.join(ASSETS_DIR, "expenses.json")

ICONS_DIR = os.path.join(ASSETS_DIR, "icons")


# icons
APP_ICON = os.path.join(ICONS_DIR, "app.png")
ADD_ICON = os.path.join(ICONS_DIR, "add.png")
BACK_ICON = os.path.join(ICONS_DIR, "back.png")
DELETE_ICON = os.path.join(ICONS_DIR, "delete.png")
SETTINGS_ICON = os.path.join(ICONS_DIR, "settings.png")
UPDATE_ICON = os.path.join(ICONS_DIR, "update.png")
EQUAL_ICON = os.path.join(ICONS_DIR, "equal.png")


class Category(StrEnum):
    """expense category enum"""

    VARIABLE = "variable"
    FIXED = "fixed"


class Comma(StrEnum):
    """comma (,) function enum"""

    FORMATTER = "formatter"
    DECIMAL = "decimal"


@dataclass(slots=True, kw_only=True)
class Expense:
    """expense item"""

    name: str
    category: Category = Category.VARIABLE
    percentage: int | float = 0.0
    amount: float = 0.0
    description: str

    def to_dict(self):
        """item to dict"""
        return asdict(self)

    def items(self):
        for field in fields(self):
            yield field.name, getattr(self, field.name)


@dataclass(slots=True, kw_only=True)
class SettingValue:
    """data class for storing Expense setting metadata"""

    widget: object
    caster: object = str

    def value(self):
        return self.caster(self.widget.text())


# expenses and their percentages
DEFAULT_SETTINGS = {
    "comma": Comma.FORMATTER,
    "expenses": [
        # fixed
        Expense(
            name="rent", description="House rent", amount=11000, category=Category.FIXED
        ),
    ],
}
