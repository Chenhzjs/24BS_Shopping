from bs4 import BeautifulSoup
import re
def soup_find(tag, str, *args):
    find_res = soup.find(tag, class_=str)
    if find_res:
        if (args):
            return find_res[args[0]]
        else:
            return find_res.get_text().strip()
    else:
        return None

content = """
<a class="doubleCardWrapper--_6NpK_ey" data-before-current-y="3197" data-spm="23" href="//detail.tmall.com/item.htm?priceTId=2147bf5617311472648075535eac66&amp;utparam=%7B%22aplus_abtest%22%3A%2260341b785f14f3471b761349cc1021e9%22%7D&amp;id=737578250115&amp;ns=1&amp;xxc=ad_ztc&amp;skuId=5795196271716" style="min-height: 400px;" target="_blank">
"""
soup = BeautifulSoup(content, 'html.parser')

pattern = r'doubleCardWrapper--........'
matches = re.findall(pattern, content)
url = soup_find("a", r"doubleCardWrapper--........", "href")
print(url)
print(matches)