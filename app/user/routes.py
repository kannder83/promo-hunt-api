import logging
import asyncio
from typing import List
from bson import ObjectId
from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks

# API
from app.user.controller import User


router: APIRouter = APIRouter(
    tags=["Users"],
    prefix="/apiv1/users"
)


@router.post(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="Create a new user",
    # response_model=models.OutPaginationUser
)
async def create_user(
    name: str,
    email: str
):
    try:

        new_user = User()

        user_status = new_user.create_user(name, email)

        return {"msg": user_status}

    except Exception as error:
        logging.error(error)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
