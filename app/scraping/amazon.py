import httpx
import logging
import asyncio
import pandas as pd
from tqdm import tqdm
from bson import ObjectId
from urllib.parse import quote
from config.conf import settings
from app.utils.utils import web_utils
from selectolax.parser import HTMLParser
from playwright.async_api import async_playwright

from app.search.controller import db_search


class AmazonScraper():
    def __init__(self, search_id: str, search_value: str):
        self.timeout = 7000
        self.search_id = search_id
        self.search_value = search_value
        self.playwright_headless = settings.playwright_headless
        self.playwright_sandbox = settings.playwright_sandbox
        self.products: list = []
        self.basic_url: str = "https://www.amazon.com"

    async def store_products(self):
        pass

    async def product_detail(self, url: str):
        async with async_playwright() as playwright:
            chromium = playwright.chromium
            browser = await chromium.launch(
                headless=self.playwright_headless,
                slow_mo=30,
                chromium_sandbox=self.playwright_sandbox
            )
            context = await browser.new_context(
                user_agent='agent',
                color_scheme='light',
                locale=r"en-US,en;q=0.9",
                viewport={'width': 1280, 'height': 1024},
                extra_http_headers=web_utils.headers('amazon')
            )
            product_description: dict = {}
            new_page = await context.new_page()
            response = await new_page.goto(self.basic_url+url, timeout=self.timeout)
            try:
                if response.status == 200:
                    # Esperar a que aparezca el selector span.a-size-large.product-title-word-break
                    await new_page.wait_for_selector('span.a-size-large.product-title-word-break', timeout=self.timeout)

                    # Se agrega al diccionaro la url
                    product_description["url"] = self.basic_url+url

                    # Obtener el contenido HTML de la página
                    html_content = await new_page.content()

                    # Utilizar Selectolax para analizar el HTML
                    tree = HTMLParser(html_content)

                    # Encontrar el elemento span.a-size-large.product-title-word-break
                    product_title_element = tree.css_first(
                        'span.a-size-large.product-title-word-break')
                    if product_title_element:
                        product_description["title"] = product_title_element.text(
                        ).strip()

                    # Encontrar el elemento #bylineInfo para la marca
                    brand_element = tree.css_first('#bylineInfo')
                    if brand_element:
                        brand_text = brand_element.text()

                        if 'Visit' in brand_text:
                            cleaned_brand_text = brand_text.replace(
                                'Visit the ', '')  # Eliminar 'Visit the '
                            product_description["brand"] = cleaned_brand_text
                        else:
                            cleaned_brand_text = brand_text.replace(
                                'Brand: ', '')  # Eliminar la etiqueta 'Brand:'
                            product_description["brand"] = cleaned_brand_text

                    # Encontrar el elemento span#acrPopover>span>a>span para las calificaciones
                    ratings_element = tree.css_first(
                        'span#acrPopover > span > a > span')
                    if ratings_element:
                        product_description["ratings"] = float(
                            ratings_element.text())

                    # Encontrar el elemento div#productDescription>p>span para la descripción
                    description_element = tree.css_first(
                        'div#productDescription > p > span')
                    if description_element:
                        product_description["description"] = description_element.text(
                        )

                    # Si cuenta con precio lo agrega
                    price_element = tree.css_first(
                        'span.a-price.a-text-price')
                    if price_element:
                        #  Solo almacena los productos que tengan precio
                        price_text = price_element.text().strip()
                        # Dividir por el símbolo de dólar
                        price_parts = price_text.split('$')
                        # Tomar el último elemento (debe ser el valor numérico)
                        cleaned_price_text = price_parts[-1]
                        price_float = float(cleaned_price_text)
                        product_description["price"] = [
                            {
                                "price": price_float,
                                "date": web_utils.get_time_now()
                            }
                        ]
                        product_description["ecommerce"] = 'amazon'

                        db_search.update_search(
                            self.search_id, product_description)

                        logging.info("Store product")

                        self.products.append(product_description)
                    await new_page.close()
                else:
                    await new_page.close()
                    raise Exception(f"Error: {response.status}")

            except Exception as error:
                await context.close()
                await browser.close()
                logging.error(f"Error: {error}")
                return {
                    "data": error,
                    "msg": "error"
                }
            await context.close()
            await browser.close()

    async def search_products(self, context) -> dict:
        url_list: list = []

        try:
            encoded_search_term: str = quote(self.search_value)

            new_page = await context.new_page()

            url = f"{self.basic_url}/s?k={encoded_search_term}&s=price-asc-rank&__mk_es_US=ÅMÅŽÕÑ&sprefix={encoded_search_term}&ref=sr_st_price-asc-rank"
            # logging.info(url)
            response = await new_page.goto(url, timeout=self.timeout)
            if response.status == 200:

                # Obtener el contenido HTML de la página
                html_content = await new_page.content()

                # Utilizar Selectolax para analizar el HTML
                tree = HTMLParser(html_content)

                # Filtrar los elementos <a> con clase específica
                link_elements = tree.css(
                    'a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')

                # Iterar sobre los elementos y obtener el valor del atributo href
                for link_element in link_elements:
                    href = link_element.attributes.get('href')
                    if href and "/sspa/" not in href:
                        url_list.append({'url': href})

                #  Se filtra para eleminiar urls duplicadas
                unique_urls = set()
                filtered_urls = []

                for item in url_list:
                    url = item.get('url')
                    if url not in unique_urls:
                        unique_urls.add(url)
                        filtered_urls.append(item)

                logging.info(f"Total URLs: {len(filtered_urls)}")
                await new_page.close()
                return {
                    "data": filtered_urls,
                    "msg": "ok"
                }
            else:
                await new_page.close()
                raise Exception(f"Status: {response.status}")

        except Exception as error:
            logging.error(f"Error: {error}")
            return {
                "data": error,
                "msg": "error"
            }

    async def obtain_products(self):
        product_url: dict = {}
        tasks: list = []
        chunk_size: int = settings.chunk_size
        try:
            async with async_playwright() as playwright:
                chromium = playwright.chromium
                browser = await chromium.launch(
                    headless=self.playwright_headless,
                    slow_mo=30,
                    chromium_sandbox=self.playwright_sandbox
                )
                context = await browser.new_context(
                    user_agent='agent',
                    color_scheme='light',
                    locale=r"en-US,en;q=0.9",
                    viewport={'width': 1280, 'height': 1024},
                    extra_http_headers=web_utils.headers('amazon')
                )

                #  Busca en la pagina princial el producto
                product_url = await self.search_products(context)
                if product_url["msg"] == "error":
                    raise Exception(product_url["data"])

                await context.close()  # Cerrar el contexto
                await browser.close()  # Cerrar el navegador

            # Crea una lista de URL de los productos

            for item in product_url["data"]:
                tasks.append(self.product_detail(item["url"]))

            # Ingresa a las url por grupos segun el chunk_size para obtener el detalle del producto
            for i in range(0, len(tasks), chunk_size):
                chunk = tasks[i:i + chunk_size]
                await asyncio.gather(*chunk[:min(chunk_size, len(tasks) - i)])

            return {
                "msg": "ok",
                "store": "amazon",
                "quantity": len(self.products)
            }

        except Exception as error:
            logging.error(f"Error: {error}")
            return {
                "data": error,
                "msg": "error",
                "store": "amazon"
            }
