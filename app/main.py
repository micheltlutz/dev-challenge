from fastapi import FastAPI
from app.database.db import engine, Base
from app.routes import auth, user


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, tags=["authentication"])

app.include_router(user.router, tags=["users"])