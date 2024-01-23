from typing import List

from fastapi import APIRouter, status, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from nashafirma_fastapi.database.db import get_db
from nashafirma_fastapi.repository import orders as repository_orders
from nashafirma_fastapi.schemas.orders import InOrder, OutOrder


router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=List[OutOrder], status_code=status.HTTP_200_OK)
async def all_orders(limit: int = Query(3, ge=0, le=100), offset: int = 0, db: Session = Depends(get_db)):
    result = await repository_orders.get_orders(limit, offset, db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="orders not found")
    return result

@router.get("/{order_id}", response_model=OutOrder, status_code=status.HTTP_200_OK)
async def view_order(order_id: int, db: Session = Depends(get_db)):
    result = await repository_orders.get_order(order_id, db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
    return result

@router.post("/", response_model=OutOrder, status_code=status.HTTP_201_CREATED)
async def create_order(body: InOrder, db: Session = Depends(get_db)):
    result = await repository_orders.create(body, db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
    return result

@router.put("/{order_id}", response_model=OutOrder, status_code=status.HTTP_201_CREATED)
async def update_order(order_id: int, body: InOrder, db: Session = Depends(get_db)):
    result = await repository_orders.update(order_id, body, db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
    return result


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_order(order_id: int, db: Session = Depends(get_db)):
    result = await repository_orders.remove(order_id, db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
    return result


@router.post("/search", response_model=List[OutOrder])
async def search(limit: int = Query(3, ge=0, le=100), offset: int = Query(0), body: InOrder = None, db: Session = Depends(get_db)):
    orders = repository_orders.search_orders(db, limit, offset, body)
    return orders


