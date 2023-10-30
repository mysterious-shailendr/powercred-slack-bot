from .manager import Manager
from ..apps.LeaveTracker.leave_tracker import LeaveTracker
import datetime
import requests
import pprint
import spacy
import re

class Llama2(Manager):
    def __init__(self):
        super().__init__()
