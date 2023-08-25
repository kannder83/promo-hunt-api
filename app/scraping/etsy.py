import logging
import requests  # httpx
import pandas as pd
from tqdm import tqdm
from bson import ObjectId
from bs4 import BeautifulSoup  # from selectolax.parser import HTMLParser


# app
from config.database import db_client
from app.utils.utils import web_utils
from app.utils.notification import notification


class ProductETSY():
    def __init__(self):
        self.list_for_scraping = []
        self.products_collection = db_client.products
        self.users_collection = db_client.users
        self.notification_data = []

    def store_data_for_scraping(self, file: str):
        """
        Lee un archivo CSV y guarda los datos en la base de datos.

        Args:
            file (str): Nombre del archivo CSV a leer.

        Raises:
            ValueError: Si las cabeceras del archivo CSV no son válidas.

        Returns:
            None
        """
        try:
            # Leer el archivo CSV
            df = pd.read_csv(f"app/data_files/{file}")

            # Verificar las cabeceras del DataFrame
            expected_headers = ["store", "name", "description", "limit", "url"]
            actual_headers = df.columns.tolist()

            if actual_headers != expected_headers:
                raise ValueError(
                    "Las cabeceras del archivo CSV no son válidas.")

            # Filtrar las filas con URLs que no existan en la colección y no estén vacías
            existing_urls = self.products_collection.distinct("url")
            df_filtered = df[~df["url"].isin(
                existing_urls) & df["url"].notna()].copy()

            # Reemplazar los valores NaN por cadenas vacías en las columnas "name" y "description"
            df_filtered.loc[:, "name"] = df_filtered["name"].fillna("")
            df_filtered.loc[:, "description"] = df_filtered["description"].fillna(
                "")

            # Validar que la columna "limit" solo contenga datos de tipo float
            if not df_filtered["limit"].apply(lambda x: isinstance(x, (int, float))).all():
                raise ValueError(
                    "La columna 'limit' no contiene solo datos de tipo float.")

            # Agregar la columna "is_active" con valor "True"
            df_filtered["is_active"] = True

            # Procesar los datos y guardarlos en la base de datos
            save_data = df_filtered.to_dict(orient='records')

            if save_data:
                all_ids = self.products_collection.insert_many(save_data)
                get_all_urls = self.products_collection.count_documents(
                    {"_id": {"$in": all_ids.inserted_ids}})
                print(f"URL >>> Se guardaron: {get_all_urls} documentos.")
            else:
                print("URL >>> No se encontraron nuevas URLs para guardar.")

        except Exception as error:
            print(f"ERROR: {error}")

    def get_url_scraping(self) -> None:
        """
        """
        try:
            dict_for_scraping: dict = {}
            query = {"store": "ETSY", "is_active": True}
            total_urls = self.products_collection.count_documents(query)
            all_urls = self.products_collection.find(query)
            for document in tqdm(all_urls, total=total_urls, desc="Obteniendo las URL"):
                dict_for_scraping = {
                    "url": document.get("url"),
                    "id": str(document.get("_id")),
                }
                self.list_for_scraping.append(dict_for_scraping)
            print("Se leen las URL de la coleccion.")
        except Exception as error:
            print(f"ERROR: {error}")

    def get_name(self, tag_name) -> str:
        """
        """
        text_name = tag_name.find(
            "h1", class_="wt-text-body-01 wt-line-height-tight wt-break-word wt-mt-xs-1")

        product_name = text_name.text
        product_name = product_name.replace('\n', '').replace('  ', '')
        return product_name

    def get_price(self, tag_price: str) -> float:
        """
        """
        products = tag_price.find('p', class_="wt-text-title-03 wt-mr-xs-1")
        products = products.text
        text_format = products.strip().replace('\n', '').replace(" ", "")
        index_money = text_format.index("$")
        price = text_format[index_money:].replace('$', '')
        return round(float(price), 2)

    def get_selected_option(self, tag_option) -> list:
        """
        """
        key_option: list = []
        value_option: list = []
        selected_option: list = []

        div_tag = tag_option.find(
            'div', attrs={'data-selector': 'listing-page-variations'})

        label_name = div_tag.find_all("div", class_="wt-validation wt-mb-xs-2")

        for key_name in label_name:
            label_tag = key_name.find(
                "label", class_="wt-label wt-display-block wt-text-caption")
            format_label = label_tag.text
            format_label = format_label.replace(
                '\n', '').replace('  ', '')
            key_option.append(format_label)

        div_wt_select = div_tag.find_all('div', class_='wt-select')

        for select_tag in div_wt_select:
            tag_select = select_tag.find(
                "select", class_="wt-select__element")
            option = tag_select.find('option', selected=True)
            option = option.text
            option = option.replace(
                '\n', '').replace('  ', '')
            value_option.append(option)

        for key, value in zip(key_option, value_option):
            option = {key: value}
            selected_option.append(option)

        return selected_option

    def validation_data(self, id: str, actual_price: float) -> None:
        """
        """
        view_data: dict = {}
        try:
            get_product = self.products_collection.find_one(
                {"_id": ObjectId(id)})

            latest_scraping_data = get_product["scraping"][-1]

            if get_product.get("limit") < actual_price:
                view_data = {
                    "id": get_product.get("_id"),
                    "store": get_product.get("store"),
                    "name": latest_scraping_data.get("name"),
                    "price": latest_scraping_data.get("price"),
                    "options": latest_scraping_data.get("options"),
                }
                self.notification_data.append(view_data)

        except Exception as error:
            print(f"ERROR: {error}")

    def store_scraping_data(self, id: str, data: dict) -> str:
        """
        """
        update_data = {"$push": {"scraping": data}}
        try:
            updated_document = self.products_collection.find_one_and_update(
                {"_id": ObjectId(id)}, update=update_data)

            return str(updated_document.get("_id"))
        except Exception as error:
            print(f"ERROR: {error}")

    def get_scraping(self) -> None:
        """
        """
        all_data: list = []
        self.get_url_scraping()

        print(f"Inicia el proceso de busqueda.")
        for url in tqdm(self.list_for_scraping, total=len(self.list_for_scraping), desc="ETSY"):

            response = requests.get(url.get("url"))

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                name = self.get_name(soup)

                price = self.get_price(soup)

                selected_option = self.get_selected_option(soup)

                scriping_data = {
                    "date": web_utils.get_time_now(),
                    "name": name,
                    "price": price,
                    "options": selected_option
                }

                updated_id = self.store_scraping_data(
                    url.get("id"), scriping_data)

                if updated_id:
                    all_data.append(updated_id)

                self.validation_data(updated_id, scriping_data.get("price"))

        if all_data:

            self.send_notification()

        print(
            f"Se actualizaron: {len(all_data)} documentos. Finaliza el proceso.")
        print(
            f"Validation: {len(self.notification_data)} productos estan por debajo del precio limite.")

    def send_notification(self):
        """
        """
        get_users = self.users_collection.find({})

        for contact in get_users:
            if contact.get("is_active"):
                notification.send_email(
                    email_receiver=contact.get("email"),
                    name_receiver=contact.get("name"),
                    data=self.notification_data
                )


product_etsy = ProductETSY()
