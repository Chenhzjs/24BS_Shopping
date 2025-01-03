from flask import request, jsonify, render_template
from werkzeug.security import check_password_hash
from . import index
from db import connection
import threading
import os

root_dir = "/Users/chenhz/Documents/work-station/BS"
def search_tags(cursor, words):
    for i in range(len(words), 0, -1):
        query = "SELECT id,title,image_url,price,url FROM products WHERE " + " AND ".join(["title LIKE %s"] * len(words[:i]))
        # print(query)
        params = tuple(['%' + word + '%' for word in words[:i]])
        print(query, params)
        cursor.execute(query, params)
        results = cursor.fetchall()
        if results:
            return results

    return []
def collect_data(web_num, keywords):

    print(f"python3 ../crawler/src/main.py {web_num} {keywords}")
    os.system(f"python3 ../crawler/src/main.py {web_num} {keywords}")

    return 0, "Data collection completed successfully"
# 登录接口
@index.route('/search', methods=['POST'])
def search():
    # print("search\nsearch\n")
    data = request.get_json()  # 获取前端发送的 JSON 数据
    user_id = data.get('id') 
    query = data.get('query')
    # if query has %
    if '%' in query:
        return jsonify({'success': False, 'message': 'Invalid query'}), 400
    # print(query)
    # split query into words by space
    words = query.split(" ")

    conn = connection.get_db_connection("Amazon")
    cursor = conn.cursor(dictionary=True)
    Amazon_res = search_tags(cursor, words)
    cursor.close()
    conn.close()
    if Amazon_res == []:
        err_code, err_msg = collect_data(0, query)
        if err_code == -1:
            return jsonify({'success': False, 'message': err_msg}), 500
        conn = connection.get_db_connection("Amazon")
        cursor = conn.cursor(dictionary=True)
        Amazon_res = search_tags(cursor, words)
        cursor.close()
        conn.close()
    # print(Amazon_res)
    conn = connection.get_db_connection("ebay")
    cursor = conn.cursor(dictionary=True)
    ebay_res = search_tags(cursor, words)
    cursor.close()
    conn.close()
    if ebay_res == []:
        err_code, err_msg = collect_data(1, query)
        if err_code == -1:
            return jsonify({'success': False, 'message': err_msg}), 500
        conn = connection.get_db_connection("ebay")
        cursor = conn.cursor(dictionary=True)
        ebay_res = search_tags(cursor, words)
        cursor.close()
        conn.close()
    # print(ebay_res)
    filtered_products = []
    for product in Amazon_res:
        filter_product = {'id'  : product['id'],
                          'title' : product['title'],
                          'url' : product['url'],
                          'image_url' : product['image_url'],
                          'price' : product['price'],
                          'platform' : "Amazon"}
        filtered_products.append(filter_product)
    for product in ebay_res:
        filter_product = {'id' : product['id'],
                          'title' : product['title'],
                          'url' : product['url'],
                          'image_url' : product['image_url'],
                          'price' : product['price'],
                          'platform' : "ebay"}
        filtered_products.append(filter_product)
    user = {'id': user_id}
    return render_template('result.html', products=filtered_products, user=user)

    
