import logging
import httpx
import pandas as pd
from tqdm import tqdm
from bson import ObjectId
from selectolax.parser import HTMLParser
from playwright.async_api import async_playwright


headers: dict = {
    'authority': 'www.mercadolibre.com.co',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'device-memory': '8',
    'downlink': '10',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}


class MercadoLibreScraper():
    def __init__(self):
        self.basic_url = "https://listado.mercadolibre.com.co"

    async def obtain_products(self, product: str):
        async with async_playwright() as playwright:
            chromium = playwright.chromium
            browser = await chromium.launch(headless=False, slow_mo=30, chromium_sandbox=True)
            context = await browser.new_context(
                user_agent='agent',
                color_scheme=r"light",
                locale=r"en-US,en;q=0.9",
                extra_http_headers=headers
            )
            page = await context.new_page()
            await page.goto(f'{self.basic_url}/nuevo/{product}_OrderId_PRICE_NoIndex_True')

            # logging.info(await page.content())
            await page.screenshot(path="ml_screenshot.png")

            await browser.close()
