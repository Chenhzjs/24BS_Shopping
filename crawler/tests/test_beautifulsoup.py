from bs4 import BeautifulSoup

# 读取 HTML 文件并解析
file_path = "product_info.txt"
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# 使用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(html_content, 'lxml')

# 打印解析后的 HTML 内容（格式化输出）
print(soup.prettify())