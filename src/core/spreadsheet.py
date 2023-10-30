from .manager import Manager
import datetime
import json

class SpreadSheetManager(Manager):
    """
    We can use GSpread for connecting to Google Spreadsheet API.
    But for now, We'll be calling Google AppScript Web Hooks.
    """
    def __init__(self):
        super().__init__()
        self.manager = Manager()