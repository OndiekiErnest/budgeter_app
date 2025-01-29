"""budgeter settings"""

import orjson

from constants import SETTINGS_FILE, DEFAULT_SETTINGS, Category, Comma, Expense


def readJSON(filename: str, default=None):
    """read json file and return data"""
    try:
        with open(filename, "rb") as file:
            loaded_data = orjson.loads(file.read())
            return loaded_data
    except Exception:  # FileNotFound
        return default


def saveJSON(filename: str, data):
    """save data to filename"""
    with open(filename, "wb") as file:
        serialized = orjson.dumps(data, option=orjson.OPT_INDENT_2)
        file.write(serialized)


def create_expense(item_data: dict):
    try:
        category = item_data.pop("category")
        return Expense(**item_data, category=Category(category))
    except Exception:
        pass


def get_settings():
    """get settings from a file or default"""
    if dict_settings := readJSON(SETTINGS_FILE):
        settings = {}

        # create expenses
        expenses = [
            item
            for item_data in dict_settings["expenses"]
            if (item := create_expense(item_data))
        ]

        settings["expenses"] = expenses or DEFAULT_SETTINGS["expenses"]

        # create comma
        settings["comma"] = (
            Comma(comma_value)
            if (comma_value := dict_settings["comma"]) in Comma
            else DEFAULT_SETTINGS["comma"]
        )
        return settings
    else:
        return DEFAULT_SETTINGS


app_settings = get_settings()


def save_settings(data: dict):
    """save items to file"""

    # convert expenses to dicts
    data["expenses"] = [item.to_dict() for item in data["expenses"]]
    try:
        saveJSON(SETTINGS_FILE, data)
    except Exception:
        pass


def parse_amt(amt: str):
    """parse user input amount"""
    if app_settings["comma"] == Comma.FORMATTER:
        # if comma is for formatting, remove it
        amt = amt.replace(",", "")

    else:
        # remove '.' coz it's used as a formatter
        amt = amt.replace(".", "")
        # if comma is used to separate decimal, replace it with a '.'
        amt = amt.replace(",", ".")
    try:
        return float(amt.replace(" ", ""))
    except Exception:
        pass


def delete_widgets(layout):
    """clear all widgets and layouts"""
    while layout.count():
        if child := layout.takeAt(0):
            if (widget := child.widget()) is not None:
                widget.deleteLater()
            else:
                delete_widgets(child.layout())
