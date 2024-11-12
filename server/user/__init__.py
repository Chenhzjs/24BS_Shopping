from flask import Blueprint
from db import connection
user = Blueprint('user', __name__)
from . import login, register, forgetPassword
