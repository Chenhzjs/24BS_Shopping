import asyncio
# from playwright.async_api import async_playwright
import json
from curl_cffi import requests

import os
from bs4 import BeautifulSoup
from .process import *
from .db import *
import sys
def scrape_amazon_curl(keyword):
    n = 3
    for i in range(0, n):
        url = f"https://www.amazon.com/s?k={keyword}&page={i}"

        page_info = requests.get(url, 
                            headers={
                                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
                            },
                            impersonate="chrome101")

        page_info = BeautifulSoup(page_info.content, 'html.parser')
        

        content_list = process_page_info(page_info)
        save_to_db(content_list)



# async def scrape_amazon(keyword):
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=False)
#         context = await browser.new_context()
        
#         page = await context.new_page()
#         # await context.route("**/*", lambda route, request: 
#         # route.abort() if request.resource_type in ["image", "font"] else route.continue_())
#         # 
#         url = f"https://www.amazon.com/s?k={keyword}"
#         await page.goto(url)
#         # await page.wait_for_load_state('load')
#         # change country to China
#         await page.wait_for_selector('#nav-global-location-popover-link')
#         await page.wait_for_timeout(1000)
#         await page.click('#nav-global-location-popover-link')
#         await page.wait_for_selector('#GLUXCountryListDropdown')
#         await page.wait_for_timeout(1000)
#         await page.click('#GLUXCountryListDropdown')
#         await page.wait_for_selector('#GLUXCountryList_0')
#         await page.wait_for_timeout(1000)
#         await page.click('#GLUXCountryList_0')
#         await page.wait_for_selector('[name="glowDoneButton"]')
#         await page.wait_for_timeout(1000)
#         await page.click('[name="glowDoneButton"]')
#         await page.wait_for_selector('.s-pagination-strip')
        
        
#         n = 2
#         for i in range(0, n):
#             await page.wait_for_timeout(10000)
#             page_info = await page.content()
#             # print(page_info)
#             page_info = BeautifulSoup(page_info, 'html.parser')
#             # print(page_info.prettify())
#             content_list = process_page_info(page_info)
#             save_to_db(content_list)
#             # change to next page
#             # next_page_bar = page_info.find('span', attrs={'class': 's-pagination-strip'})
#             # next_page_bott = next_page_bar.find('li', attrs={'class': 'a-last'})
#             if i == n - 1:
#                 break
#             await page.wait_for_selector("a:has-text('下一页')")
#             await page.wait_for_timeout(1000)
#             await page.click("a:has-text('下一页')")
#             await page.wait_for_selector('.s-pagination-strip')

#         await browser.close()

def amazon_run(keyword):
    keyword = keyword.strip()
    scrape_amazon_curl(keyword)
