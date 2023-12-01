import os

from dotenv import load_dotenv
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse

load_dotenv()
router = APIRouter()


@router.get("/")
def redirect_to_docs():
    response = RedirectResponse(url='/docs')
    return response


@router.get("/health-check")
def health_check():
    return JSONResponse(
        content={"status": "ok"},
        status_code=status.HTTP_200_OK
    )


@router.get("/version")
def health_check():
    return JSONResponse(
        content={"version": os.getenv("VERSION")},
        status_code=status.HTTP_200_OK
    )
