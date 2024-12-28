import mysql.connector
import platform


if platform.system() == "Windows":
    db_password = ""
else:
    db_password = ""    

db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': db_password,  
    'database': ''
}

def get_db_connection(database):
    db_config['database'] = database
    connection = mysql.connector.connect(**db_config)
    return connection