from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, RedirectResponse

from app.config import VERSION

router = APIRouter()


@router.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs")


@router.get("/health-check")
def health_check():
    return JSONResponse(
        content={"status": "ok"},
        status_code=status.HTTP_200_OK,
    )


@router.get("/version")
def version():
    return JSONResponse(
        content={"version": VERSION},
        status_code=status.HTTP_200_OK,
    )
