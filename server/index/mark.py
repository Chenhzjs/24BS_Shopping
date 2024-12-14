from flask import Flask, request, jsonify
from db import connection
from . import index


@index.route('/mark', methods=['POST'])
def mark_item():
    data = request.get_json()
    identifier = data.get('user_id')
    item_id = data.get('id')
    platform = data.get('platform')
    marked = data.get('marked')
    # print(data)
    # return jsonify({'status': 'success'})
    # print(item_id, marked)
    conn = connection.get_db_connection("user")
    cursor = conn.cursor()
    if "@" in identifier:  # 如果输入的是邮箱
        cursor.execute("SELECT id FROM users WHERE email = %s", (identifier,))
    else:  # 如果输入的是用户名
        cursor.execute("SELECT id FROM users WHERE username = %s", (identifier,))
    user_id = cursor.fetchone()
    user_id = user_id[0]
    if marked:
        cursor.execute("REPLACE INTO marked_items (id, platform, uuid) VALUES (%s, %s, %s)", (user_id, platform, item_id))
        print("insert")
    else:
        cursor.execute("DELETE FROM marked_items WHERE id = %s AND uuid = %s", (user_id, item_id))
        print("delete")
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'status': 'success'})