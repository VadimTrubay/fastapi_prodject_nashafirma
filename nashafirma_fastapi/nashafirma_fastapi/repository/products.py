from sqlalchemy.orm import Session

from nashafirma_fastapi.database.models import Product
from nashafirma_fastapi.schemas.products import InProduct


# async def get_product_by_id(product_id: int, db: Session):
#     product = db.query(Product).filter_by(id=product_id).first()
#     return product

async def get_products(limit: int, offset: int, db: Session):
    products = db.query(Product).order_by(Product.product).limit(limit).offset(offset).all()
    return products

async def get_product(product_id: int, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()
    return product

async def create(body: InProduct, db: Session):
    product = Product(**body.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

async def update(product_id: int, body: InProduct, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        product.product = body.product
        product.price = body.price
        db.commit()
    return product

async def remove(product_id: int, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    return product