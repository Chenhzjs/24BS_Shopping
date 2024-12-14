from flask import Blueprint
from db import connection
index = Blueprint('index', __name__)
from . import search
from . import mail
from . import mark
from . import price_curve