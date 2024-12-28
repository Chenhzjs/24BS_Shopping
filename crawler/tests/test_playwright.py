import asyncio
from playwright.async_api import async_playwright
import json
import os
from bs4 import BeautifulSoup

COOKIES_FILE = "taobao_cookies.json"

async def save_cookies(page):
    cookies = await page.context.cookies()
    with open(COOKIES_FILE, 'w') as file:
        json.dump(cookies, file)
    print("Cookies 已保存！")

async def load_cookies(context):
    if os.path.exists(COOKIES_FILE):
        with open(COOKIES_FILE, 'r') as file:
            cookies = json.load(file)
        print("Cookies = ", cookies)
        await context.add_cookies(cookies)
        print("Cookies 已加载！")

async def login_taobao():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await load_cookies(context)

        await page.goto("https://login.taobao.com/")
        await page.wait_for_timeout(20000)  

        if "taobao.com" in page.url:
            print("登录成功！")
            await save_cookies(page)
        else:
            print("登录失败，请检查账号信息或手动解决验证码。")

        await browser.close()

async def scrape_taobao(keyword):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        
        await load_cookies(context)
        
        page = await context.new_page()
        await context.route("**/*", lambda route, request: 
        route.abort() if request.resource_type in ["image", "font"] else route.continue_())
        # https://www.ebay.com/sch/i.html?_nkw=phone&_sacat=0&_fcid=45
        # https://www.amazon.com/s?k=phone&__mk_zh_CN=亚马逊网站&crid=1G3TEXHHJHP9J&sprefix=pho,aps,412&ref=nb_sb_noss_2
        url = f"https://s.taobao.com/search?q={keyword}"
        await page.goto(url)
        await page.wait_for_load_state('load')
        
        await page.wait_for_timeout(5000)  
        # await page.keyboard.press('Meta+Alt+I')

        # await page.keyboard.press('Meta+F')
        # await page.keyboard.type('"ice-container"')
        
        # await page.wait_for_selector('"ice-container"')
        # print("元素已找到！")

        # await page.keyboard.press('Enter')
        # input("Press Enter to continue...")
        # await page.wait_for_load_state('load')  # 等待页面加载完成
        # await page.wait_for_timeout(500000)  # 等待页面加载完成
        # await page.wait_for_load_state('networkidle')
        # await page.wait_for_selector('#root', timeout=10000) 
        page_info = await page.content()
        print(page_info)
        page_info = BeautifulSoup(page_info, 'html.parser').prettify()
        # print(page_info)
        with open("product_info.txt", "w") as file:
            file.write(page_info)
        print("商品信息已保存！")


        await browser.close()


if __name__ == "__main__":

    # asyncio.run(login_taobao())
    

    keyword = "手机"
    asyncio.run(scrape_taobao(keyword))