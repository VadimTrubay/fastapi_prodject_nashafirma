import time

from fastapi import FastAPI, Path, Query, Depends, HTTPException, Request
from sqlalchemy.orm import Session

# from nasha_firma_fastapi.database.models import Product
# from nasha_firma_fastapi.database.db import get_db
# from nasha_firma_fastapi.schemas import ProductModel, ResponseProductModel

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# @app.get("/api/healthchecker")
# def healthchecker(db: Session = Depends(get_db)):
#     try:
#         # Make request
#         result = db.execute("SELECT 1").fetchone()
#         if result is None:
#             raise HTTPException(status_code=500, detail="Database is not configured correctly")
#         return {"message": "Welcome to FastAPI!"}
#     except Exception as e:
#         print(e)
#         raise HTTPException(status_code=500, detail="Error connecting to the database")


@app.get("/contact/{contact_id}")
async def index(contact_id: int):
    return {"contact": contact_id}


# @app.post("/add_product")
# async def add_product(product: ProductModel, db: Session = Depends(get_db())):
#     new_product = Product(name=product.name, price=product.price)
#     db.add(new_product)
#     db.commit()
#     db.refresh(new_product)
#     return new_product
#
#
# @app.get("/products")
# async def all_products(skip: int = 0, limit: int = Query(default=10, le=100, ge=10), db: Session = Depends(get_db)):
#     products = db.query(Product).offset(skip).limit(limit).all()
#     return products
#
#
# @app.get("/products/{product_id}", response_model=ResponseProductModel)
# async def read_note(product_id: int = Path(description="The ID of the product to get", gt=0, le=10),
#                     db: Session = Depends(get_db)):
#     product = db.query(Product).filter(Product.id == product_id).first()
#     if product is None:
#         raise HTTPException(status_code=500, detail='Not found')
#     return product


