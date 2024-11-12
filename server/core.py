import yaml
import os
from flask import Flask
from flask_cors import CORS
from user import user
from db import connection
def create_core():
    # 创建 Flask 应用
    core = Flask(__name__)
    CORS(core)

    # 注册蓝图
    core.register_blueprint(user, url_prefix='/user')
    print(core.url_map)
    return core

core = create_core()

def create_tables():
    conn = connection.get_db_connection('user')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255),
        email VARCHAR(255),
        password VARCHAR(255),
        recover_code VARCHAR(10)
    )
    """)
    cursor.close()
    conn.close()
if __name__ == '__main__':
    create_tables()
    core.run(debug=True, host='0.0.0.0', port=5001)