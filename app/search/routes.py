import logging
from bson import ObjectId
from fastapi import APIRouter, HTTPException, status, BackgroundTasks, Query, Path

# APP
from app.user.controller import db_user
from app.search.controller import db_search
from app.background_process.process import search_process, tracking_products_process


router: APIRouter = APIRouter(
    tags=["Search"],
    prefix="/apiv1/search"
)


@router.get(
    path="/all",
    status_code=status.HTTP_200_OK,
    summary="Get all search documents",
    # response_model=models.OutPaginationUser
)
async def get_all_search(
    limit: int = 10,
    skip: int = 0
):
    try:
        search_documents = db_search.get_all_search(limit, skip)

        if search_documents['msg'] == 'error':
            raise Exception(search_documents['data'])

        return search_documents

    except Exception as error:
        logging.error(error)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.get(
    path="/detail/{search_id}",
    status_code=status.HTTP_200_OK,
    summary="Get search by ID"
)
async def get_search_by_id(search_id: str):
    try:
        search_info = db_search.search_by_id(search_id)
        if search_info["msg"] == "error":
            raise Exception(search_info["data"])

        return search_info

    except Exception as error:
        logging.error(error)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.get(
    path="/products/{search_id}",
    status_code=status.HTTP_200_OK,
    summary="Get products by search ID"
)
async def products_by_search_id(
    search_id: str,
):
    try:
        products = db_search.get_products_by_search_id(search_id)

        if products['msg'] == 'error':
            raise Exception(products['data'])

        return products

    except Exception as error:
        logging.error(error)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.post(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="Search",
    # response_model=models.OutPaginationUser
)
async def search_in_pages(
    background_tasks: BackgroundTasks,
    search: str,
    user_id: str
):
    try:
        # Se busca que exista el usuario creado
        get_user = db_user.search_user(user_id)
        if get_user["msg"] == "error":
            raise Exception(get_user["data"])

        #  Se crea el ObjectId del search
        search_id = db_search.create_search(search, user_id)
        if not isinstance(search_id, ObjectId):
            raise Exception('Not create a search ID')

        #  Se crean las tareas de busqueda en segundo plano
        background_tasks.add_task(search_process, search_id, search, user_id)

        return {
            "msg": "Se recibe la solicitud correctamente.",
            "data": {
                "search_id": str(search_id)
            }
        }

    except Exception as error:
        logging.error(error)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.post(
    path="/tracking/{search_id}",
    status_code=status.HTTP_200_OK,
    summary="tracking",
    # response_model=models.OutPaginationUser
)
async def tracking_products(
    search_id: str,
    background_tasks: BackgroundTasks
):
    try:
        # Se valida que exista el search_id
        search = db_search.search_by_id(search_id)
        if search["msg"] == "error":
            raise Exception(search["data"])

        # Se obtiene el diccionario con las url para hacer seguimiento
        products = db_search.get_products_by_search_id(search_id)
        if products['msg'] == 'error':
            raise Exception(products['data'])

        #  Se crean las tareas de seguimiento en segundo plano
        background_tasks.add_task(
            tracking_products_process, products)

        return {
            "msg": "Se recibe la solicitud de seguimiento correctamente.",
            "data": {
                "search_id": str(search_id),
                "total_products": len(products['data'])
            }
        }

    except Exception as error:
        logging.error(error)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.delete(
    path="/{search_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a search by search_id"
)
async def delete_search_by_id(
    search_id: str,
):
    try:
        delete_result = db_search.delete_search_by_id(search_id)
        if delete_result['msg'] == 'error':
            raise Exception(delete_result['data'])

        return delete_result

    except Exception as error:
        logging.error(error)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
