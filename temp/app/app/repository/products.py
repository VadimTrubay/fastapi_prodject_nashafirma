from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.app_db import get_db
from app.database.models import Product, User
from app.schemas.products import InProduct


async def get_product_by_id(product_id: int, db: AsyncSession = Depends(get_db)):
    product = db.query(Product).filter_by(id=product_id).first()
    return product

async def get_products(limit: int, offset: int, db: AsyncSession = Depends(get_db)):
    products = db.query(Product).order_by(Product.product).limit(limit).offset(offset).all()
    return products

async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await  get_product_by_id(product_id, db)
    return product

async def create(body: InProduct, db: AsyncSession = Depends(get_db)):
    product = Product(**body.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

async def update(product_id: int, body: InProduct, db: AsyncSession = Depends(get_db)):
    product = await  get_product_by_id(product_id, db)
    if product:
        product.product = body.product
        product.price = body.price
        db.commit()
    return product

async def remove(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await  get_product_by_id(product_id, db)
    if product:
        db.delete(product)
        db.commit()
    return product


def search_products(db: AsyncSession = Depends(get_db), limit: int = 10, offset: int = 0, body: InProduct = None):
    query = db.query(Product)
    if body:
        if body.product:
            query = query.filter(Product.product.like(f"%{body.product}%"))
        if body.price:
            query = query.filter(Product.price.like(f"%{body.price}%"))

    products = query.offset(offset).limit(limit).all()
    return products