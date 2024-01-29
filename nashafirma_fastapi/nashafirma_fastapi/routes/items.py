from typing import List

from fastapi import APIRouter, status, Depends, Query, HTTPException
from nashafirma_fastapi.database.db import get_db
from nashafirma_fastapi.repository import items as repository_items
from nashafirma_fastapi.schemas.items import ItemModel, ItemResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/{order_id}",
            response_model=List[ItemResponse],
            status_code=status.HTTP_200_OK
            )
async def all_items_by_order(
        order_id: int,
        limit: int = Query(3, ge=0, le=100),
        offset: int = 0, db: Session = Depends(get_db)
):
    result = await repository_items.get_items_by_order(order_id, limit, offset, db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="items not found")
    return result


@router.post("/",
             response_model=ItemResponse,
             status_code=status.HTTP_201_CREATED
             )
async def create_item(
        body: ItemModel,
        db: Session = Depends(get_db)
):
    result = await repository_items.create(body, db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
    return result


@router.put("/{item_id}",
            response_model=ItemResponse,
            status_code=status.HTTP_201_CREATED
            )
async def update_item(
        item_id: int,
        body: ItemModel,
        db: Session = Depends(get_db)
):
    result = await repository_items.update(item_id, body, db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
    return result


@router.delete("/{item_id}",
               status_code=status.HTTP_204_NO_CONTENT
               )
async def remove_item(
        item_id: int,
        db: Session = Depends(get_db)
):
    result = await repository_items.remove(item_id, db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
    return result
