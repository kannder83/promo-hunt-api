import logging
import asyncio
from typing import List
from bson import ObjectId
from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks

# APP
from app.search.controller import db_search
from app.scraping.amazon import AmazonScraper


router: APIRouter = APIRouter(
    tags=["Search"],
    prefix="/apiv1/search"
)


async def search_process(search_id: str, value: str) -> None:
    """
    """
    try:
        amazon = AmazonScraper(search_id, value)

        tasks = [
            amazon.obtain_products(),
            # task2()
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

        logging.info(f"Finaliza el proceso de busqueda.")
        db_search.update_search_status(search_id, "finished")

    except Exception as error:
        logging.error(error)


@router.post(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="Search",
    # response_model=models.OutPaginationUser
)
async def search_in_pages(
    search: str,
    background_tasks: BackgroundTasks
):
    try:

        search_id = db_search.create_search(search)
        if not isinstance(search_id, ObjectId):
            raise Exception('Not create a search ID')

        background_tasks.add_task(search_process, search_id, search)

        return {
            "msg": "Se recibe la solicitud correctamente.",
            "data": {
                "search_id": str(search_id)
            }
        }

    except Exception as error:
        logging.error(error)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
