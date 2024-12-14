from flask import request, jsonify, render_template
from werkzeug.security import check_password_hash
from . import user
from db import connection

# 登录接口
@user.route('/profile', methods=['POST'])
def profile():
    data = request.get_json()  # 获取前端发送的 JSON 数据
    identifier = data.get('username')  # 用户名或邮箱
    # print(identifier)
    conn = connection.get_db_connection("user")
    cursor = conn.cursor(dictionary=True)

    if "@" in identifier:  
        cursor.execute("SELECT id FROM users WHERE email = %s", (identifier,))
    else:  # 如果输入的是用户名
        cursor.execute("SELECT id FROM users WHERE username = %s", (identifier,))
    user_index = cursor.fetchone() 
    user_id = user_index['id']
    # print(user_id)
    cursor.execute("SELECT platform, uuid FROM marked_items WHERE id = %s", (user_id,))
    marked_products = cursor.fetchall()
    cursor.close()
    conn.close()
    products = []
    for marked_product in marked_products:
        if marked_product['platform'] == '0':
            conn = connection.get_db_connection("Amazon")
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id,title,price,url FROM products WHERE id = %s", (marked_product['uuid'],))
            products_tmp = cursor.fetchall()
            cursor.close()
            conn.close()
            products.append(products_tmp[-1])
        else:
            conn = connection.get_db_connection("ebay")
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id,title,price,url FROM products WHERE id = %s", (marked_product['uuid'],))
            products_tmp = cursor.fetchall()
            cursor.close()
            conn.close()
            products.append(products_tmp[-1])

    user_id_map = {'id': identifier}
    return render_template('profile.html', user=user_id_map, products=products)