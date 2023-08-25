import logging
from fastapi import FastAPI
from config.conf import settings
from fastapi.middleware.cors import CORSMiddleware


# Routes
from app.search.routes import router as search_router
from app.user.routes import router as user_router


def get_application():

    api_conf: dict = {
        "title": "DEV: PromoHuntAPI",
        "description": "DEV: PromoHuntAPI",
        "version": "0.9.0",
        "root_path": settings.dev_url,
        "docs_url": settings.dev_url
    }

    origins: list = ["*"]

    if settings.mode_prod:
        api_conf: dict = {
            "title": "PromoHuntAPI",
            "description": "PromoHuntAPI",
            "version": settings.version,
            "root_path": settings.prod_url,
            "docs_url": settings.prod_url
        }

        origins: list = settings.allowed_hosts

    app: FastAPI = FastAPI(
        title=api_conf["title"],
        description=api_conf["description"],
        docs_url=api_conf["docs_url"],
        version=api_conf["version"],
        root_path=api_conf["root_path"]
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    @app.on_event("startup")
    def startup_event():

        if settings.debug:
            logging.basicConfig(
                level=logging.DEBUG,
                format="%(asctime)s %(levelname)s %(funcName)s %(message)s"
            )
        else:
            logging.basicConfig(
                level=logging.WARNING,
                format="%(asctime)s %(levelname)s %(funcName)s %(message)s"
            )

    # Routes to publish
    app.include_router(search_router)
    app.include_router(user_router)

    return app


application = get_application()
