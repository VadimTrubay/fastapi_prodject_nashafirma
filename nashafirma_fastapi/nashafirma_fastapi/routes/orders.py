from typing import List

from fastapi import APIRouter, status, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from nashafirma_fastapi.database.db import get_db
from nashafirma_fastapi.database.models import User
from nashafirma_fastapi.repository import orders as repository_orders
from nashafirma_fastapi.schemas.orders import OrderModel, OrderResponse, OrderCreate
from services.auth import auth_service

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/by_admin",
            response_model=List[OrderResponse],
            status_code=status.HTTP_200_OK
            )
async def all_orders_by_admin(
        limit: int = Query(3, ge=0, le=100),
        offset: int = 0,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
):
    result = await repository_orders.get_orders_by_admin(limit, current_user, offset, db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orders not found")
    return result


@router.get("/by_user",
            response_model=List[OrderResponse],
            status_code=status.HTTP_200_OK
            )
async def all_orders_by_users(
        limit: int = Query(3, ge=0, le=100),
        offset: int = 0,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
):
    result = await repository_orders.get_orders_by_user(limit, current_user, offset, db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orders not found")
    return result


@router.post("/search",
             response_model=List[OrderResponse]
             )
async def search(
        db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user),
        limit: int = Query(3, ge=0, le=100),
        offset: int = 0,
        query: str | None = None
):
    result = repository_orders.search_orders(db, current_user, limit, offset, query)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return result


# @router.get("/{order_id}",
#             response_model=OrderResponse,
#             status_code=status.HTTP_200_OK
#             )
# async def view_order(
#         order_id: int,
#         db: Session = Depends(get_db)
# ):
#     result = await repository_orders.get_order(order_id, db)
#     if result is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
#     return result


@router.post("/",
             response_model=OrderCreate,
             status_code=status.HTTP_201_CREATED
             )
async def create_order(
        body: OrderModel,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
):
    result = await repository_orders.create(body, current_user, db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return result


@router.put("/{order_id}",
            response_model=OrderResponse,
            status_code=status.HTTP_201_CREATED
            )
async def update_order(
        order_id: int,
        body: OrderModel,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
):
    result = await repository_orders.update(order_id, current_user, body, db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return result


@router.delete("/{order_id}",
               status_code=status.HTTP_204_NO_CONTENT
               )
async def remove_order(
        order_id: int,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
):
    result = await repository_orders.remove(order_id, current_user, db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return result
