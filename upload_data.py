from app.scraping.etsy import product_etsy


def main():
    """
    """
    file_name = input("Ingrese el nombre del archivo: ")
    product_etsy.store_data_for_scraping(file_name)


if __name__ == "__main__":
    main()
