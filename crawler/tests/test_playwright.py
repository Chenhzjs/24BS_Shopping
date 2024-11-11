import asyncio
from playwright.async_api import async_playwright
import json
import os
from bs4 import BeautifulSoup

COOKIES_FILE = "taobao_cookies.json"

async def save_cookies(page):
    # 保存登录后的 Cookies 到本地文件
    cookies = await page.context.cookies()
    with open(COOKIES_FILE, 'w') as file:
        json.dump(cookies, file)
    print("Cookies 已保存！")

async def load_cookies(context):
    # 如果本地存在 Cookies 文件，加载到浏览器上下文
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

        # 加载 Cookies 如果已存在
        await load_cookies(context)

        # 访问淘宝登录页面
        await page.goto("https://login.taobao.com/")
        await page.wait_for_timeout(20000)  # 等待用户手动输入验证码和登录

        # 检查是否已登录成功（例如检查用户昵称）
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
        
        # 加载已保存的 Cookies
        await load_cookies(context)
        
        page = await context.new_page()
        await context.route("**/*", lambda route, request: 
        route.abort() if request.resource_type in ["image", "font"] else route.continue_())
        url = f"https://s.taobao.com/search?q={keyword}"
        await page.goto(url)
        await page.wait_for_load_state('load')
        
        await page.wait_for_timeout(5000)  # 等待页面加载完成
        # await page.keyboard.press('Meta+Alt+I')

        # # 搜索 "ice-container"（模拟 Command + F）
        # await page.keyboard.press('Meta+F')
        # await page.keyboard.type('"ice-container"')
        
        # # 等待元素显示并选中
        # await page.wait_for_selector('"ice-container"')
        # print("元素已找到！")

        # # 复制选中的元素（模拟右键复制）
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
        # 爬取商品信息并保存到文件
        with open("product_info.txt", "w") as file:
            file.write(page_info)
        print("商品信息已保存！")
        # 爬取商品信息

        await browser.close()

# 运行脚本
if __name__ == "__main__":
    # 首次登录淘宝
    # asyncio.run(login_taobao())
    
    # 使用已保存的 Cookies 进行爬取
    keyword = "手机"
    asyncio.run(scrape_taobao(keyword))