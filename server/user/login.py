from flask import request, jsonify
from werkzeug.security import check_password_hash
from . import user
from db import connection

# 登录接口
@user.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # 获取前端发送的 JSON 数据
    identifier = data.get('username')  # 用户名或邮箱
    password = data.get('password')

    # # 检查用户名或邮箱和密码是否为空
    # if not identifier or not password:
    #     return jsonify({'success': False, 'message': '用户名或邮箱和密码不能为空'}), 400

    conn = connection.get_db_connection("user")
    cursor = conn.cursor(dictionary=True)

    # 根据输入判断是用户名还是邮箱
    if "@" in identifier:  # 如果输入的是邮箱
        cursor.execute("SELECT * FROM users WHERE email = %s", (identifier,))
    else:  # 如果输入的是用户名
        cursor.execute("SELECT * FROM users WHERE username = %s", (identifier,))

    user = cursor.fetchone()  # 获取查询到的第一个用户记录

    cursor.close()
    conn.close()

    # 验证密码
    if user and check_password_hash(user['password'], password):  # 使用哈希密码进行验证
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': '用户名、邮箱或密码错误'}), 401