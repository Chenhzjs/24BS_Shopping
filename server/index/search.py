from flask import request, jsonify
from werkzeug.security import check_password_hash
from . import index
from db import connection

# 登录接口
@index.route('/login', methods=['POST'])
def search():
    data = request.get_json()  # 获取前端发送的 JSON 数据
