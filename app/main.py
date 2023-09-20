from fastapi import FastAPI
from app.database.db import engine, Base
from app.routes import auth, user
import logging

app = FastAPI()


def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        logging.info("Database initialized successfully.")
    except Exception as e:
        logging.error(f"Error initializing the database: {e}")


@app.on_event("startup")
async def startup_event():
    init_db()


app.include_router(auth.router, tags=["authentication"])

app.include_router(user.router, tags=["users"])
