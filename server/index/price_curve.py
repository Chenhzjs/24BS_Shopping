from flask import request, jsonify, render_template
from werkzeug.security import check_password_hash
from . import index
from db import connection
import threading
import os

def get_price_data(uid):
    # check if is Amazon
    conn = connection.get_db_connection("Amazon")
    cursor = conn.cursor()
    query = "SELECT price, time FROM products WHERE id = %s ORDER BY time"
    cursor.execute(query, (uid,))
    data = cursor.fetchall()
    if not data:
        # check if is eBay
        conn = connection.get_db_connection("ebay")
        cursor = conn.cursor()
        query = "SELECT price, time FROM products WHERE id = %s ORDER BY time"
        cursor.execute(query, (uid,))
        data = cursor.fetchall()
    cursor.close()
    conn.close()

    
    price_data = [{"time": row[1], "price": row[0]} for row in data]
    return price_data

@index.route('/price_curve', methods=['POST'])
def price_curve():
    data = request.get_json()
    uid = data.get('uid')
    price_data = get_price_data(uid)
    
    return jsonify({'price_data': price_data})