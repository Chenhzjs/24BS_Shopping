from urllib.parse import unquote
url_str = 'https://www.amazon.com/s?k=phone&__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&crid=1G3TEXHHJHP9J&sprefix=pho%2Caps%2C412&ref=nb_sb_noss_2'
paras = unquote(url_str)
print(paras)
