import mysql.connector
import platform


if platform.system() == "Windows":
    db_password = "Hz040719"
else:
    db_password = ""    

# 数据库配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': db_password,  
    'database': ''
}

# 获取数据库连接
def get_db_connection(database):
    db_config['database'] = database
    connection = mysql.connector.connect(**db_config)
    return connection