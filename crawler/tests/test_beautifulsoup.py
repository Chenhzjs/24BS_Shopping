from bs4 import BeautifulSoup

file_path = "product_info.txt"
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'lxml')

print(soup.prettify())