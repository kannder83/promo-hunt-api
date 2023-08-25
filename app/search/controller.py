import logging
from bson import ObjectId
from config.database import db_client


class DbSearch():
    def __init__(self):
        self.searches_collection = db_client.searches

    def create_search(self, search: str) -> ObjectId:
        try:
            if not search:
                raise Exception("Empty search")

            result = self.searches_collection.insert_one(
                {
                    "search_proyect": search,
                    "status": "in progress",
                })

            return result.inserted_id
        except Exception as error:
            logging.error(f"Error: {error}")
            return {
                "data": error,
                "msg": "error"
            }

    def update_search(self, search_id: str, data: dict) -> dict:
        try:
            query = {"_id": ObjectId(search_id)}

            result = self.searches_collection.update_one(
                query,
                {"$push": {"products": data}}
            )

            search_project = self.searches_collection.find_one(
                result.upserted_id)

            return search_project

        except Exception as error:
            logging.error(f"Error: {error}")
            return {
                "data": error,
                "msg": "error"
            }

    def update_search_status(self, search_id: str, status: str):
        try:
            query = {"_id": ObjectId(search_id)}

            result = self.searches_collection.update_one(
                query,
                {"$set": {"status": status}}
            )

            search_project = self.searches_collection.find_one(
                result.upserted_id)

            if not search_project:
                raise Exception("Not found")

            return {
                "data": "updated",
                "msg": "ok"
            }

        except Exception as error:
            logging.error(f"Error: {error}")
            return {
                "data": error,
                "msg": "error"
            }

    def update_search_ecommerce_status(self, search_id: str, status: str, store: str):
        try:
            query = {"_id": ObjectId(search_id)}

            result = self.searches_collection.update_one(
                query,
                {"$push": {"stores": {store: status}}}
            )

            search_project = self.searches_collection.find_one(
                result.upserted_id)

            if not search_project:
                raise Exception("Not found")

            return {
                "data": "updated",
                "msg": "ok"
            }

        except Exception as error:
            logging.error(f"Error: {error}")
            return {
                "data": error,
                "msg": "error"
            }


db_search = DbSearch()
