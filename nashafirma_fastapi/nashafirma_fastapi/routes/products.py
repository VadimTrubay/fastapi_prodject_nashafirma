from typing import List

from fastapi import APIRouter, status, Depends, Query, HTTPException
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from nashafirma_fastapi.database.db import get_db
from nashafirma_fastapi.repository import products as repository_products
from nashafirma_fastapi.schemas.products import InProduct, OutProduct

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[OutProduct])
async def all_products(limit: int = Query(3, le=100), offset: int = 0, db: Session = Depends(get_db)):
    result = await repository_products.get_products(limit, offset, db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return result

@router.get("/{product_id}", response_model=OutProduct)
async def view_product(product_id: int, db: Session = Depends(get_db)):
    result = await repository_products.get_product(product_id, db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return result

@router.post("/", response_model=OutProduct)
async def create_product(body: InProduct, db: Session = Depends(get_db)):
    result = await repository_products.create(body, db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return result

@router.put("/{product_id}", response_model=OutProduct)
async def update_product(product_id: int, body: InProduct, db: Session = Depends(get_db)):
    result = await repository_products.update(product_id, body, db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return result

@router.delete("/{product_id}", response_model=OutProduct)
async def remove_product(product_id: int, db: Session = Depends(get_db)):
    result = await repository_products.remove(product_id, db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return result