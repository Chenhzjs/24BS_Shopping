import yaml
import os
from flask import Flask
from flask_cors import CORS
from user import user
from index import index
from db import connection

def create_core():

    core = Flask(__name__)
    CORS(core)

    core.register_blueprint(user, url_prefix='/user')
    core.register_blueprint(index, url_prefix='/index')
    print(core.url_map)
    return core

core = create_core()

def create_tables():
    conn = connection.get_db_connection('Amazon')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        pid INT AUTO_INCREMENT PRIMARY KEY,
        id VARCHAR(255),
        title VARCHAR(255),
        url TEXT,
        image_url TEXT,
        star VARCHAR(50),
        customer VARCHAR(100),
        price VARCHAR(50),
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
    """)
    cursor.close()
    conn.close()

    conn = connection.get_db_connection('ebay')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        pid INT AUTO_INCREMENT PRIMARY KEY,
        id VARCHAR(255),
        title VARCHAR(255),
        url TEXT,
        image_url TEXT,
        star VARCHAR(50),
        customer VARCHAR(100),
        price VARCHAR(50),
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
    """)
    cursor.close()
    conn.close()

    conn = connection.get_db_connection('user')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255),
        email VARCHAR(255),
        password VARCHAR(255),
        recover_code VARCHAR(10),
        recover_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS marked_items (
        pid INT AUTO_INCREMENT PRIMARY KEY,
        id INT,
        platform VARCHAR(255),
        uuid VARCHAR(255)
    )
    """)
    cursor.close()
    conn.close()
if __name__ == '__main__':
    create_tables()
    core.run(debug=True, host='0.0.0.0', port=5001)