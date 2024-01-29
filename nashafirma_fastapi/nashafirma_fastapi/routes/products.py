from typing import List

from fastapi import APIRouter, status, Depends, Query, HTTPException
from nashafirma_fastapi.database.db import get_db
from nashafirma_fastapi.database.models import User
from nashafirma_fastapi.repository import products as repository_products
from nashafirma_fastapi.schemas.products import ProductModel, ProductResponse
from services.auth import auth_service
from sqlalchemy.orm import Session

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[ProductResponse], status_code=status.HTTP_200_OK)
async def all_products(
        limit: int = Query(10, ge=0, le=100), offset: int = 0, db: Session = Depends(get_db)
):
    result = await repository_products.get_products(limit, offset, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return result


@router.post("/search", response_model=List[ProductResponse])
async def search_products(
        db: Session = Depends(get_db),
        limit: int = Query(10, ge=0, le=100),
        offset: int = 0,
        query: str | None = None,
):
    result = repository_products.search_products(db, limit, offset, query)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return result


@router.get(
    "/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK
)
async def view_product(product_id: int, db: Session = Depends(get_db)):
    result = await repository_products.get_product(product_id, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return result


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
        body: ProductModel,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db),
):
    result = await repository_products.create(body, current_user, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not credential"
        )
    return result


@router.put(
    "/{product_id}", response_model=ProductResponse, status_code=status.HTTP_201_CREATED
)
async def update_product(
        product_id: int,
        body: ProductModel,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db),
):
    result = await repository_products.update(product_id, current_user, body, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return result


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_product(
        product_id: int,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db),
):
    result = await repository_products.remove(product_id, current_user, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return result
