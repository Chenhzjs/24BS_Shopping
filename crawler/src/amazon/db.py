import mysql.connector

def save_to_db(iterms):
    # 配置数据库连接
    connection = mysql.connector.connect(
        host="localhost",      # 替换为你的数据库主机地址
        user="root",      # 替换为你的数据库用户名
        password="Hz040719",  # 替换为你的数据库密码
        database="Amazon"   # 替换为你的数据库名称
    )

    cursor = connection.cursor()

    # 创建表结构
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        url TEXT,
        image_url TEXT,
        star VARCHAR(50),
        customer VARCHAR(100),
        price VARCHAR(50)
    )
    """)

    # 要插入的数据
    for iterm in iterms:
        data = iterm

        # 插入数据的 SQL 语句
        sql = """
        INSERT INTO products (title, url, image_url, star, customer, price)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        # 执行插入
        cursor.execute(sql, (data['title'], data['url'], data['image_url'], data['star'], data['customer'], data['price']))
        connection.commit()

        print("1 行数据插入成功！")

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
    