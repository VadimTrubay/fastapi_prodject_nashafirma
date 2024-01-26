from typing import List

from fastapi import APIRouter, status, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database.app_db import get_db
from app.repository import items as repository_items
from app.schemas.items import InItem, OutItem


router = APIRouter(prefix="/items", tags=["items"])



@router.get("/{order_id}", response_model=List[OutItem], status_code=status.HTTP_200_OK)
async def all_items(order_id: int, limit: int = Query(3, ge=0, le=100), offset: int = 0, db: Session = Depends(get_db)):
    result = await repository_items.get_items(order_id, limit, offset, db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="items not found")
    return result


@router.post("/", response_model=OutItem, status_code=status.HTTP_201_CREATED)
async def create_item(body: InItem, db: Session = Depends(get_db)):
    result = await repository_items.create(body, db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
    return result

@router.put("/{item_id}", response_model=OutItem, status_code=status.HTTP_201_CREATED)
async def update_item(item_id: int, body: InItem, db: Session = Depends(get_db)):
    result = await repository_items.update(item_id, body, db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
    return result


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_item(item_id: int, db: Session = Depends(get_db)):
    result = await repository_items.remove(item_id, db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
    return result

