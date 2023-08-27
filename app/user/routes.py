import logging
from fastapi import APIRouter, HTTPException, status, Query

# API
from app.user.controller import db_user


router: APIRouter = APIRouter(
    tags=["Users"],
    prefix="/apiv1/users"
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="Get a list of users",
)
async def get_users(
    limit: int = Query(default=10, le=100,
                       description="Number of users to return"),
    skip: int = Query(default=0, ge=0, description="Number of users to skip")
):
    try:
        users_list = db_user.get_users(limit, skip)

        return users_list

    except Exception as error:
        logging.error(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.post(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="Create a new user",
)
async def create_user(
    name: str,
    email: str
):
    try:
        user_status = db_user.create_user(name, email)

        if user_status["msg"] == "error":
            raise Exception(user_status["data"])

        return user_status

    except Exception as error:
        logging.error(error)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.delete(
    path="/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a user by user_id"
)
async def delete_user(user_id: str):
    try:
        delete_result = db_user.delete_user(user_id)

        if delete_result['msg'] == 'error':
            raise Exception(delete_result['data'])

        return delete_result

    except Exception as error:
        logging.error(error)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
