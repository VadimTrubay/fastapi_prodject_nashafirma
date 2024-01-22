import time

import redis.asyncio as redis
from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy import text
from sqlalchemy.orm import Session
from nashafirma_fastapi.utils.py_logger import get_logger
from fastapi.middleware.cors import CORSMiddleware
from nashafirma_fastapi.conf.config import settings
from fastapi_limiter import FastAPILimiter

from nashafirma_fastapi.routes import orders, products, items, users, auth
from nashafirma_fastapi.database.db import get_db

app = FastAPI()
origins = ["*"]
# logger = get_logger(__name__)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!", "stage": "database is OK!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


# @app.on_event("startup")
# async def startup():
#     r = await redis.Redis(
#         host=settings.redis_host,
#         port=settings.redis_port,
#         password=settings.redis_password,
#         db=0,
#         encoding="utf-8",
#         decode_responses=True,
#     )
#     await FastAPILimiter.init(r)


app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
app.include_router(items.router, prefix="/api")