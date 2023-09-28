from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.contact.contact_schema import Contact

router = APIRouter()


@router.post("/contact/")
async def create_contact(contact: Contact):
    message = f"""Thank {contact.name}, for getting in touch and sharing your interests,
    look forward to hearing from you soon."""

    return JSONResponse(
        content={'msg': message},
        status_code=status.HTTP_200_OK
    )