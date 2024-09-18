import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError, FastAPIError
import uvicorn
from sqlalchemy.exc import InvalidRequestError
from starlette.exceptions import HTTPException as StarletteHttpException
from api.v1.utils.database import Base, engine
from api.v1.responses.success_responses import success_response
from api.v1.responses.error_responses import ValidationErrorResponse, ErrorResponse

load_dotenv()

# Creating database
Base.metadata.create_all(bind=engine)

# App settings for project
app = FastAPI(
    title="BookVault",
    summary="Library management api",
    version="0.0.1",
    contact={
        "name": "Izzyjosh",
        "email": "joshuajosephizzyjosh@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    debug=os.environ.get("DEBUG") != "False",
    redoc_url=None,
    docs_url="/docs",
)

# Setting up cors and middleware
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Setup error responses
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    errors = []
    for error in exc.errors():
        errors.append({"field": error.get("loc")[-1], "message": error.get("msg")})

    response = ValidationErrorResponse(errors=errors)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=response.model_dump()
    )


@app.exception_handler(StarletteHttpException)
async def http_exception_handler(request: Request, exc: StarletteHttpException):
    """
    :param request: HTTP request object
    :param exc: HTTP exception
    :returns JSONResponse
    """

    response = ErrorResponse(status_code=exc.status_code, message=exc.detail)
    return JSONResponse(status_code=exc.status_code, content=response.model_dump())


@app.exception_handler(InvalidRequestError)
async def http_exception_handler(request: Request, exc: InvalidRequestError):
    """
    :param request: HTTP request object
    :param exc: HTTP exception
    :returns JSONResponse
    """

    response = ErrorResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=exc._message()
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response.model_dump()
    )


@app.exception_handler(FastAPIError)
async def http_exception_handler(request: Request, exc: FastAPIError):
    """
    :param request: HTTP request object
    :param exc: HTTP exception
    :returns JSONResponse
    """

    response = ErrorResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=exc.detail
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response.model_dump()
    )


@app.get("/")
async def home():
    return success_response(status_code=200, message="Welcome to BookVault API")


# start server

if __name__ == "__main__":
    uvicorn.run(app, port=int(os.environ.get("SERVER_PORT", 5001)), reload=False)
