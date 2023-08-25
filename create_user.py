from app.user.controller import User


def main():
    """
    """
    new_user = User()

    name: str = input("Ingrese el nombre: ")
    email: str = input("Ingrese el email: ")

    user_status = new_user.create_user(name, email)

    print(user_status)


if __name__ == "__main__":
    main()
