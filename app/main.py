import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.exception_handlers import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
import logging
from api.main import router as main_router
from api.auth import auth_router
from api.product import product_router

load_dotenv()
environ = os.getenv("environment")

app = FastAPI()
logger = logging.getLogger(__name__)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.exception_handler(NoResultFound)
async def database_exception_handler(request, exc):
    logger.exception(
        "database Error, record not found for request %s ",
        str(exc),
        request.url,
    )
    if environ != "prod":
        return await http_exception_handler(request, HTTPException(404, str(exc)))

    return await http_exception_handler(request, HTTPException(404, "Data Not Found"))


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request, exc):
    logger.exception(
        "database Error response %s while requesting %s ",
        str(exc),
        request.url,
    )
    if environ != "prod":
        return await http_exception_handler(request, HTTPException(422, str(exc)))

    return await http_exception_handler(request, HTTPException(422, "Database Error"))


@app.exception_handler(TypeError)
@app.exception_handler(ZeroDivisionError)
async def validation_exception_handler(request, exc):
    logger.exception(
        "Validation Error response %s while requesting %s ",
        str(exc),
        request.url,
    )
    if environ != "prod":
        return await http_exception_handler(request, HTTPException(422, str(exc)))
    return await http_exception_handler(
        request, HTTPException(422, "Error Occurred , check logs for more details")
    )


@app.exception_handler(Exception)
async def all_exception_handler(request, exc):
    logger.exception(
        "Error response %s while requesting %s ",
        str(exc),
        request.url,
    )
    if environ != "prod":
        return await http_exception_handler(request, HTTPException(400, str(exc)))
    return await http_exception_handler(
        request, HTTPException(400, "Error Occurred , check logs for more details")
    )


@app.get("/health")
async def check_health():
    return {"code": status.HTTP_200_OK, "status": "Working Fine"}


app.include_router(main_router, tags=["root"])
app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(product_router, prefix="/api", tags=["product"])
