from nashafirma_fastapi.database.models import Product, User
from nashafirma_fastapi.schemas.products import ProductModel
from sqlalchemy import or_, Text, cast
from sqlalchemy.orm import Session


async def get_product_by_id(product_id: int, db: Session):
    product = db.query(Product).filter_by(id=product_id).first()
    return product


async def get_products(limit: int, offset: int, db: Session):
    products = (
        db.query(Product).order_by(Product.product).limit(limit).offset(offset).all()
    )
    return products


async def get_product(product_id: int, db: Session):
    product = await get_product_by_id(product_id, db)
    return product


async def create(body: ProductModel, current_user: User, db: Session):
    product = Product(**body.model_dump())
    if product:
        if current_user.is_superuser:
            db.add(product)
            db.commit()
            db.refresh(product)
            return product


async def update(product_id: int, current_user: User, body: ProductModel, db: Session):
    product = await get_product_by_id(product_id, db)
    if product:
        if current_user.is_superuser:
            product.product = body.product
            product.price = body.price
            db.commit()
            return product


async def remove(product_id: int, current_user: User, db: Session):
    product = await get_product_by_id(product_id, db)
    if product:
        if current_user.is_superuser:
            db.delete(product)
            db.commit()
            return product


def search_products(db: Session, limit: int = 10, offset: int = 0, query: str = None):
    if query:
        products = (
            db.query(Product)
            .filter(
                or_(
                    Product.product.ilike(f"%{query}%"),
                    cast(Product.price, Text).ilike(f"%{query}%"),
                )
            )
            .limit(limit)
            .offset(offset)
            .all()
        )
        return products
