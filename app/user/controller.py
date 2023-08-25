from bson import ObjectId
from config.database import db_client


class User():
    def __init__(self):
        self.users_collection = db_client.users

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
                return f"Email no válido, revisar."

            new_user = self.users_collection.insert_one(
                new_user)

            new_user_id = new_user.inserted_id

            get_user = self.users_collection.find_one(
                {"_id": ObjectId(new_user_id)})

            return f"Se creo el usuario: '{get_user.get('name')}' email: '{get_user.get('email')}'"

        except ValueError as error:
            return f"Error: {error}"
        except Exception as error:
            return f"Error: {error}"
