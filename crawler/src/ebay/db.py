import mysql.connector
import platform

if platform.system() == "Windows":
    db_password = ""  
else:
    db_password = ""    

def save_to_db(iterms):
    
    connection = mysql.connector.connect(
        host="127.0.0.1",      
        user="root",      
    
        password=db_password,  
        database="ebay"   
    )


    cursor = connection.cursor()

    t = 0
    for iterm in iterms:
        t = t + 1
        data = iterm

        sql = """
        INSERT INTO products (id, title, url, image_url, star, customer, price)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (data['id'], data['title'], data['url'], data['image_url'], data['star'], data['customer'], data['price']))
        connection.commit()


    print(f"{t} 行数据插入成功！")

    cursor.close()
    connection.close()

def print_all_from_db():
    connection = mysql.connector.connect(
        host="127.0.0.1",    
        user="root",      
        password=db_password,  
        database="ebay"   
    )
    
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM products")
    
    records = cursor.fetchall()
    
    for record in records:
        print(record)
    