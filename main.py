import time
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session

from nashafirma_fastapi.database.db import get_db
from nashafirma_fastapi.routes import orders, products, items, users, auth
from nashafirma_fastapi.utils.py_logger import get_logger

app = FastAPI()
origins = ["*"]
logger = get_logger(__name__)

app.add_middleware(
    CORSMiddleware,  # noqa
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    # logger.info(f"{request.method} {request.url} {response.status_code} {process_time}")
    return response


BASE_DIR = Path(".")

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "nashafirma_fastapi" / "static"),
    name="static",
)

app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(items.router, prefix="/api")
app.include_router(orders.router, prefix="/api")

# @app.on_event("startup")
# async def startup():
#     r = redis.Redis(host=settings.redis_host, port=settings.redis_port)
#     await FastAPILimiter.init(r)


templates = Jinja2Templates(directory=BASE_DIR / "nashafirma_fastapi" / "templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "title": "Nashafirma"}
    )


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"message": "Welcome to FastAPI!", "stage": "database is OK!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")
