import asyncio
from playwright.async_api import async_playwright
import json
import os
from bs4 import BeautifulSoup
from process import *
from db import *
import sys
async def scrape_amazon(keyword):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        
        page = await context.new_page()
        # await context.route("**/*", lambda route, request: 
        # route.abort() if request.resource_type in ["image", "font"] else route.continue_())
        # 
        url = f"https://www.amazon.com/s??language=zh_CN&currency=USD&k={keyword}&__mk_zh_CN=亚马逊网站"
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
        await page.wait_for_timeout(10000)
        
        
        
        for i in range(0, 3):
            page_info = await page.content()
            # print(page_info)
            page_info = BeautifulSoup(page_info, 'html.parser')
            print(page_info.prettify())
            # 爬取商品信息并保存到文件
            content_list = process_page_info(page_info)
            save_to_db(content_list)
            # change to next page
            # next_page_bar = page_info.find('span', attrs={'class': 's-pagination-strip'})
            # next_page_bott = next_page_bar.find('li', attrs={'class': 'a-last'})
            await page.wait_for_selector("a:has-text('下一页')")
            await page.wait_for_timeout(1000)
            await page.click("a:has-text('下一页')")
            await page.wait_for_selector('.s-pagination-strip')
            await page.wait_for_timeout(10000)
            
        # print_all_from_db()
        # with open("product_info.txt", "w") as file:
        #     file.write(page_info)
        # print("商品信息已保存！")
        # 爬取商品信息

        await browser.close()

# 运行脚本
def amazon_run(keyword):
    asyncio.run(scrape_amazon(keyword))

