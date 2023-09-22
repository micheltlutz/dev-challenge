import logging
from fastapi import FastAPI
from app.database.db import engine, Base
from fastapi.middleware.cors import CORSMiddleware

# Importing routes
from app.authentication import auth_routes
from app.user import user_routes
from app.statement import statement_routes
from app.balance import balance_routes
from app.contact import contact_routes

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite qualquer origem. Não faça isso em produção!
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos. Você pode ajustar isso dependendo das suas necessidades
    allow_headers=["*"],
)


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
app.include_router(balance_routes.router, tags=["balance"])
app.include_router(contact_routes.router, tags=["contact"])
