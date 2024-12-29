from flask import request, jsonify, render_template
from werkzeug.security import check_password_hash
from . import user
from db import connection

@user.route('/login', methods=['POST'])
def login():
    data = request.get_json()  
    identifier = data.get('username')  
    password = data.get('password')

    conn = connection.get_db_connection("user")
    cursor = conn.cursor(dictionary=True)

    if "@" in identifier:  
        cursor.execute("SELECT * FROM users WHERE email = %s", (identifier,))
    else:  
        cursor.execute("SELECT * FROM users WHERE username = %s", (identifier,))

    user = cursor.fetchone()  

    cursor.close()
    conn.close()
    if user is None:
        return jsonify({'success': False, 'message': '用户名、邮箱或密码错误'}), 401
    user_id = {'id': user['username']}
    
    if user and check_password_hash(user['password'], password):  
        return render_template('search.html', user=user_id)
    return jsonify({'success': False, 'message': '用户名、邮箱或密码错误'}), 401