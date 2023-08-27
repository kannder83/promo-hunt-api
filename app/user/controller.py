import logging
from bson import ObjectId
from config.database import db_client


class User():
    def __init__(self):
        self.users_collection = db_client.users

    def search_user(self, user_id: str) -> dict:
        """
        """
        try:
            get_user = get_user = self.users_collection.find_one(
                {"_id": ObjectId(user_id)})

            if not get_user:
                raise Exception(f"UserID {user_id} does not exist")

            return {
                "data": get_user,
                "msg": "ok"
            }

        except Exception as error:
            logging.error(f"Error: {error}")
            return {
                "data": error,
                "msg": "error"
            }

    def create_user(self, name: str, email: str):
        """
        """
        new_user: dict = {}
        try:
            if not name:
                raise ValueError("El nombre no puede estar vacío.")
            if not email:
                raise ValueError("El correo electrónico no puede estar vacío.")

            get_user = self.users_collection.find_one({"email": email})

            if get_user:
                return f"El correo {email} ya existe."

            new_user = {
                "name": name,
                "email": email,
                "is_active": True
            }

            if "@" not in new_user.get("email"):
                raise Exception(f"Email no válido, revisar.")

            new_user = self.users_collection.insert_one(
                new_user)

            get_user = self.users_collection.find_one(
                {"_id": ObjectId(new_user.inserted_id)})

            return {
                "data": "Se creo el usuario correctamente.",
                "user_id": str(new_user.inserted_id),
                "msg": "ok"
            }

        except ValueError as error:
            logging.error(f"Error: {error}")
            return {
                "data": error,
                "msg": "error"
            }
        except Exception as error:
            logging.error(f"Error: {error}")
            return {
                "data": error,
                "msg": "error"
            }

    def delete_user(self, user_id: str) -> dict:
        """
        Elimina un usuario por su user_id.
        """
        try:
            result = self.users_collection.delete_one(
                {"_id": ObjectId(user_id)})

            if result.deleted_count == 0:
                raise Exception(f"UserID {user_id} does not exist")

            return {
                "data": f"Usuario con user_id {user_id} eliminado correctamente.",
                "user_id": user_id,
                "msg": "ok"
            }

        except Exception as error:
            logging.error(f"Error: {error}")
            return {
                "data": error,
                "msg": "error"
            }

    def get_users(self, limit: int = 10, skip: int = 0) -> dict:
        """
        Retorna una lista de usuarios con opciones de limit y skip.
        """
        serialize_users: list = []
        try:
            users_cursor = self.users_collection.find(
                {}).limit(limit).skip(skip)
            users_list = list(users_cursor)

            logging.info(f"users_list: {users_list}")

            for user in users_list:
                user['user_id'] = str(user['_id'])
                del user['_id']
                serialize_users.append(user)

            return {
                "data": serialize_users,
                "total_users": len(serialize_users),
                "msg": "ok"
            }

        except Exception as error:
            logging.error(f"Error: {error}")
            return {
                "data": error,
                "msg": "error"
            }


db_user = User()
