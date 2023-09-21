import logging
from fastapi import FastAPI
from app.database.db import engine, Base

# Importing routes
from app.authentication import auth_routes
from app.user import user_routes
from app.statement import statement_routes


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


app.include_router(auth_routes.router, tags=["authentication"])
app.include_router(user_routes.router, tags=["users"])
app.include_router(statement_routes.router, tags=["statement"])
