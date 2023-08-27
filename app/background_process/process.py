import time
import asyncio
import logging
from app.user.controller import db_user
from app.search.controller import db_search
from app.scraping.amazon import AmazonScraper
from app.utils.notification import notification
from app.scraping.mercadolibre import MercadoLibreScraper


async def search_process(search_id: str, value: str, user_id: str) -> None:
    """
    """
    try:
        start_time = time.time()  # Captura el tiempo de inicio

        amazon = AmazonScraper(search_id, value)
        mercadolibre = MercadoLibreScraper(search_id, value)

        tasks = [
            amazon.obtain_products(),
            mercadolibre.obtain_products()
        ]
        results = await asyncio.gather(*tasks)

        logging.info(f"Results: {results}")

        for scraping in results:
            if scraping['msg'] == "ok" and scraping['quantity'] != 0:
                db_search.update_search_ecommerce_status(
                    search_id, "finished", scraping['store'])
            elif scraping['msg'] == "ok" and scraping['quantity'] == 0:
                db_search.update_search_ecommerce_status(
                    search_id, "Not found data", scraping['store'])
            else:
                db_search.update_search_ecommerce_status(
                    search_id, "error", scraping['store'])

        end_time = time.time()  # Captura el tiempo de finalización
        # Calcula el tiempo transcurrido en segundos
        elapsed_time = end_time - start_time

        # Se actualiza el estado en la base de datos
        db_search.update_search_status(search_id, "finished")

        # Se buscan los datos del usuario
        user = db_user.search_user(user_id)

        #  Se envia correo de notificación
        notification.send_email(
            email_receiver=user['data']['email'],
            name_receiver=user['data']['name'],
            description=f'El proceso de consulta ha finalizado. Tiempo: {round(elapsed_time, 2)}',
            subject="Proceso finalizado: Busqueda de Productos",
            data=results
        )
        logging.info(
            f"Finaliza el proceso de busqueda. Tiempo: {round(elapsed_time, 2)}")

    except Exception as error:
        logging.error(error)


async def tracking_products_process(products: dict) -> None:
    """
    """
    tasks: list = []
    try:
        start_time = time.time()  # Captura el tiempo de inicio
        # Se instancias las clases
        amazon = AmazonScraper(products["search_id"])
        mercadolibre = MercadoLibreScraper(products["search_id"])

        # Se actualiza el estado en la base de datos
        db_search.update_search_status(products["search_id"], "updating")

        # Del diccionaro products crear una lista de urls por ecommerce
        for product in products['data']:

            # Se crean las tareas
            if product['products']['ecommerce'] == 'amazon':
                result = await amazon.update_product(product['products']['url'], product['products']['product_id'])
                tasks.append(result)

            if product['products']['ecommerce'] == 'mercadolibre':
                result = await mercadolibre.update_product(product['products']['url'], product['products']['product_id'])
                tasks.append(result)

        end_time = time.time()  # Captura el tiempo de finalización
        # Calcula el tiempo transcurrido en segundos
        elapsed_time = end_time - start_time

        # Se busca con el search_id el user_id
        user = db_search.search_by_id(products["search_id"])

        user_id = user['data']['user_id']

        # Se buscan los datos del usuario
        user = db_user.search_user(user_id)

        #  Se envia correo de notificación
        notification.send_email(
            email_receiver=user['data']['email'],
            name_receiver=user['data']['name'],
            description=f'El proceso de consulta ha finalizado. Tiempo {round(elapsed_time, 2)}',
            subject="Proceso finalizado: Actualización de precios",
            data=[
                {'total_urls': len(tasks), "total_time": round(elapsed_time, 2)}]
        )
        # Se actualiza el estado en el documento de la base de datos
        db_search.update_search_status(products["search_id"], "finished")
        logging.info(
            f"Finaliza el proceso de busqueda. Tiempo {round(elapsed_time, 2)}")
    except Exception as error:
        logging.error(error)
