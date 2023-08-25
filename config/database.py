from pymongo import MongoClient
from config.conf import settings


URL = f"mongodb://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/admin"

if settings.mode_prod:
    db_client = MongoClient(URL).web_scraping
else:
    db_client = MongoClient(URL).dev_web_scraping
