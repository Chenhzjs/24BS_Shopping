import asyncio
from playwright.async_api import async_playwright
import json
import os
from bs4 import BeautifulSoup

async def scrape_amazon(keyword):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        
        page = await context.new_page()
        # await context.route("**/*", lambda route, request: 
        # route.abort() if request.resource_type in ["image", "font"] else route.continue_())
        # 
        url = f"https://www.amazon.com/s?k={keyword}&__mk_zh_CN=亚马逊网站"
        await page.goto(url)
        # await page.wait_for_load_state('load')
        # change country to China
        await page.wait_for_selector('#nav-global-location-popover-link')
        await page.wait_for_timeout(1000)
        await page.click('#nav-global-location-popover-link')
        await page.wait_for_selector('#GLUXCountryListDropdown')
        await page.wait_for_timeout(1000)
        await page.click('#GLUXCountryListDropdown')
        await page.wait_for_selector('#GLUXCountryList_0')
        await page.wait_for_timeout(1000)
        await page.click('#GLUXCountryList_0')
        await page.wait_for_selector('[name="glowDoneButton"]')
        await page.wait_for_timeout(1000)
        await page.click('[name="glowDoneButton"]')
        await page.wait_for_selector('.s-pagination-strip')
        await page.wait_for_timeout(5000)
        
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
    keyword = "phone"
    asyncio.run(scrape_amazon(keyword))

