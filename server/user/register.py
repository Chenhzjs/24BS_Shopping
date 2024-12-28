from flask import request, jsonify
from werkzeug.security import generate_password_hash
from . import user
from db import connection


@user.route('/register', methods=['POST'])
def register():
    data = request.get_json()  
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    print(username, email, password)

    # if not username or not email or not password:
    #     return jsonify({'success': False, 'message': '用户名、邮箱和密码不能为空'}), 400


    conn = connection.get_db_connection("user")
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
    user = cursor.fetchone()

    if user:
        return jsonify({'success': False, 'message': '用户名或邮箱已存在'}), 400


    if len(password) < 6:
        return jsonify({'success': False, 'message': '密码长度不能小于 6 位'}), 400
    if not password.isalnum():
        return jsonify({'success': False, 'message': '密码只能包含数字和字母'}), 400
    

    cursor.execute(
        "INSERT INTO users (username, email, password, recover_time) VALUES (%s, %s, %s, NULL)",
        (username, email, generate_password_hash(password)) 
    )
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({'success': True, 'message': '注册成功'})