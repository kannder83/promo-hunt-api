import httpx
import logging
import asyncio
from bson import ObjectId
from config.conf import settings
from app.utils.utils import web_utils
from selectolax.parser import HTMLParser
from app.search.controller import db_search
from playwright.async_api import async_playwright


class MercadoLibreScraper():
    def __init__(self, search_id: str, search_value: str = None):
        self.timeout = settings.timeout
        self.search_id = search_id
        self.search_value = search_value
        self.playwright_headless = settings.playwright_headless
        self.playwright_sandbox = settings.playwright_sandbox
        self.products: list = []
        self.basic_url: str = "https://listado.mercadolibre.com.co"

    async def update_product(self, url: str, product_id: str) -> dict:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=web_utils.headers('mercadolibre'))

                if response.status_code == 200:
                    tree = HTMLParser(response.text)

                    # Se agrega el precio
                    price_element = tree.css_first(
                        'div.ui-pdp-price__main-container')
                    if price_element:
                        price_string = price_element.text()
                        # Obtener el valor numérico después del último "$"
                        price_string = price_string.split("$")[-1]
                        price_numeric = float(price_string.replace(
                            ".", "").replace(",", ""))  # Convertir a float

                        tracking_price = {
                            "price": price_numeric,
                            "date": web_utils.get_time_now()
                        }

                        #  Se actualiza el producto con nuevo registro de fecha y hora
                        db_search.update_search_product(
                            self.search_id, product_id, tracking_price)

                        logging.info("Updated product: Mercadolibre")

                        return {
                            "msg": "ok",
                            "data": {"ecommerce": "mercadolibre"}
                        }
                else:
                    raise Exception(f"Error: {response.status}")

        except Exception as error:
            logging.error(f"Error: {error}")
            return {
                "msg": "error",
                "data": error
            }

    async def product_detail(self, url: str) -> None:
        product_description: dict = {}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=web_utils.headers('mercadolibre'))

                if response.status_code == 200:
                    # Se agrega la URL de product
                    product_description["url"] = url

                    tree = HTMLParser(response.text)

                    # Encontrar el elemento para el title
                    product_title_element = tree.css_first('.ui-pdp-title')
                    if product_title_element:
                        product_description["title"] = product_title_element.text(
                        ).strip()

                    # Se agrega la Marca
                    product_description["brand"] = "marca"

                    # Se agrega el rating
                    product_description["ratings"] = "ratings"

                    # Se agrega la descripción
                    product_description['description'] = "description"
                    # Se agrega el product_id
                    product_description['product_id'] = str(ObjectId())

                    # Se agrega el precio
                    price_element = tree.css_first(
                        'div.ui-pdp-price__main-container')
                    if price_element:
                        price_string = price_element.text()
                        # Obtener el valor numérico después del último "$"
                        price_string = price_string.split("$")[-1]
                        price_numeric = float(price_string.replace(
                            ".", "").replace(",", ""))  # Convertir a float
                        product_description["price"] = [
                            {
                                "price": price_numeric,
                                "date": web_utils.get_time_now()
                            }
                        ]

                        #  Se agrega el ecommerce
                        product_description["ecommerce"] = 'mercadolibre'

                        db_search.update_search(
                            self.search_id, product_description)

                        logging.info("Store product: Mercadolibre")

                        self.products.append(product_description)
                else:
                    raise Exception(f"Error: {response.status}")

        except Exception as error:
            logging.error(f"Error: {error}")

    async def search_products(self, context) -> dict:
        url_list: list = []

        try:
            encoded_search_term: str = self.search_value.replace(' ', '-')
            if not encoded_search_term:
                raise Exception("There is no value for the search term.")

            new_page = await context.new_page()

            url: str = f'{self.basic_url}/{encoded_search_term}'

            response = await new_page.goto(url, timeout=self.timeout)
            if response.status == 200:

                # Obtener el contenido HTML de la página
                html_content = await new_page.content()

                # Utilizar Selectolax para analizar el HTML
                tree = HTMLParser(html_content)

                for a_element in tree.css('div.ui-search-result__card a.ui-search-link'):
                    href = a_element.attributes.get("href")
                    url_list.append({'url': href})

                # Crear una lista para almacenar las URLs únicas y válidas
                filtered_urls = []

                # Crear un conjunto para almacenar las URLs ya vistas
                seen_urls = set()

                for item in url_list:
                    url = item.get('url', '')  # Obtener la URL del diccionario

                    # Verificar si la URL es única y no contiene "www"
                    if url not in seen_urls and "www" not in url and "click1." not in url:
                        filtered_urls.append({'url': url})
                        # Agregar la URL al conjunto de URLs vistas
                        seen_urls.add(url)

                # Verificar la cantidad de elementos de la lista
                if len(filtered_urls) > 20:
                    # Tomar los primeros elementos
                    filtered_urls = filtered_urls[:20]
                else:
                    # Tomar todos los elementos de la lista
                    filtered_urls = filtered_urls[:]

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

    async def obtain_products(self) -> dict:
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
                    extra_http_headers=web_utils.headers('mercadolibre')
                )

                # Busca en la pagina princial el producto
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
                    "store": "mercadolibre",
                    "quantity": len(self.products)
                }
        except Exception as error:
            logging.error(f"Error: {error}")
            return {
                "data": error,
                "msg": "error",
                "store": "mercadolibre"
            }
