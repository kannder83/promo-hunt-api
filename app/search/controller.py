import logging
from bson import ObjectId
from config.database import db_client


class DbSearch():
    def __init__(self):
        self.searches_collection = db_client.searches

    def create_search(self, search: str, user_id: str) -> ObjectId:
        try:
            if not search:
                raise Exception("Empty search")

            result = self.searches_collection.insert_one(
                {
                    "search_proyect": search,
                    "status": "in progress",
                    "user_id": user_id
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

            return {
                "data": search_project,
                "msg": "ok"
            }

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
                "data": search_project,
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
                "data": search_project,
                "msg": "ok"
            }

        except Exception as error:
            logging.error(f"Error: {error}")
            return {
                "data": error,
                "msg": "error"
            }

    def search_by_id(self, search_id: str) -> dict:
        try:
            query = {"_id": ObjectId(search_id)}
            search_document = self.searches_collection.find_one(query)

            if not search_document:
                raise Exception(f"SearchID {search_id} not found")

            search_document['search_id'] = str(search_document['_id'])
            del search_document['_id']

            return {
                "data": search_document,
                "msg": "ok"
            }

        except Exception as error:
            logging.error(f"Error: {error}")
            return {
                "data": error,
                "msg": "error"
            }

    def get_all_search(self, limit: int = 10, skip: int = 0) -> dict:
        try:
            pipeline = [
                {
                    "$project": {
                        "search_proyect": 1,
                        "status": 1,
                        "products_count": {"$size": "$products"}
                    }
                },
                {"$skip": skip},
                {"$limit": limit}
            ]

            search_documents = self.searches_collection.aggregate(pipeline)

            results = list(search_documents)
            for document in results:
                document['search_id'] = str(document['_id'])
                del document['_id']

            return {
                "data": results,
                "total_searches": len(results),
                "msg": "ok"
            }

        except Exception as error:
            logging.error(f"Error: {error}")
            return {
                "data": error,
                "msg": "error"
            }

    def get_products_by_search_id(self, search_id: str) -> dict:
        try:
            pipeline = [
                {"$match": {"_id": ObjectId(search_id)}},
                {"$unwind": "$products"},
                {"$project": {
                    "_id": 0,
                    "products.product_id": 1,
                    "products.url": 1,
                    "products.ecommerce": 1,
                }}
            ]

            search_result = list(self.searches_collection.aggregate(pipeline))

            if not search_result:
                raise Exception("No products found.")

            return {
                "data": search_result,
                "total_searches": len(search_result),
                "search_id": search_id,
                "msg": "ok"
            }

        except Exception as error:
            logging.error(f"Error: {error}")
            return {
                "data": error,
                "msg": "error"
            }

    def delete_search_by_id(self, search_id: str) -> dict:
        try:
            query = {"_id": ObjectId(search_id)}
            result = self.searches_collection.delete_one(query)

            if result.deleted_count == 0:
                raise Exception(f"SearchId {search_id} not found")

            return {
                "data": "Search deleted successfully",
                "search_id": search_id,
                "msg": "ok"
            }

        except Exception as error:
            logging.error(f"Error: {error}")
            return {
                "data": error,
                "msg": "error"
            }

    def update_search_product(self, search_id: str, product_id: str, new_price: dict):
        try:

            result = self.searches_collection.update_one(
                {"_id": ObjectId(search_id),
                 "products.product_id": product_id},
                {"$push": {"products.$.price": new_price}}
            )

            if result.modified_count == 0:
                raise Exception("Product not found")

            search_project = self.searches_collection.find_one(
                result.upserted_id)

            if not search_project:
                raise Exception("Not found")

            return {
                "data": search_project,
                "msg": "ok"
            }
        except Exception as error:
            logging.error(f"Error: {error}")
            return {
                "data": error,
                "msg": "error"
            }


db_search = DbSearch()
