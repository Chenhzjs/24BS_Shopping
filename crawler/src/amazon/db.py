import mysql.connector
import platform

# 根据操作系统设置不同的密码
if platform.system() == "Windows":
    db_password = "Hz040719"  # Windows 下的密码
else:
    db_password = ""    # macOS 下的密码

def save_to_db(iterms):
    # 配置数据库连接
    connection = mysql.connector.connect(
        host="localhost",      # 替换为你的数据库主机地址
        user="root",      # 替换为你的数据库用户名
        password=db_password,  # 替换为你的数据库密码
        database="Amazon"   # 替换为你的数据库名称
    )

    cursor = connection.cursor()



    # 要插入的数据
    t = 0
    for iterm in iterms:
        t = t + 1
        data = iterm

        # 插入数据的 SQL 语句
        sql = """
        INSERT INTO products (id, title, url, image_url, star, customer, price)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        # 执行插入
        cursor.execute(sql, (data['id'], data['title'], data['url'], data['image_url'], data['star'], data['customer'], data['price']))
        connection.commit()

    print(f"{t} 行数据插入成功！")

    cursor.close()
    connection.close()

def print_all_from_db():
    # 配置数据库连接
    connection = mysql.connector.connect(
        host="localhost",      # 替换为你的数据库主机地址
        user="root",      # 替换为你的数据库用户名
        password="Hz040719",  # 替换为你的数据库密码
        database="Amazon"   # 替换为你的数据库名称
    )
    
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM products")
    
    # 获取所有记录
    records = cursor.fetchall()
    
    for record in records:
        print(record)
    