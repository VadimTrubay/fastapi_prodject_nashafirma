# FastApi project nashafirma

- this is a good Fastapi project

# How to start for developers:
- update project from Git repository https://github.com/VadimTrubay/fastapi_prodject_nashafirma.git
- create environment
- poetry export --without-hashes --format requirements.txt --output requirements.txt
- pip install -r requirements.txt
- create in root folder your own .env file like .env.example 
- run docker application
- run in terminal: `docker-compose up` -> up REdis+Postgress
- run in terminal: `alembic upgrade head` -> implementation current models to DB
- run in terminal: `uvicorn main:app --host localhost --port 8000 --reload` -> start application
- now you have access to:
- http://127.0.0.1:8000/docs -> Swagger documentation
- http://127.0.0.1:8000/redoc -> Redoc documentation
- http://127.0.0.1:8000/ -> template


### After changes in DB models:
- `alembic revision --autogenerate -m "name"` -> generation of migration
- `alembic upgrade head` -> implementation to DB

### Shut off
- terminal with uvicorn -> Press CTRL+C to quit
- terminal with docker run: `docker-compose down` -> shut Redis+Postgres

## Already implemented functionality FastApi:
- error handler
- performance meter
- root - for template generation
- healthchecker - for check DB status
- connection limiter
- authentication JWT mechanism 
- forget password mechanism
