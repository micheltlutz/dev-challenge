import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.authentication import auth_routes
from app.balance import balance_routes
from app.config import CORS_ALLOW_ORIGINS, LOG_LEVEL, PROJECT_NAME, VERSION
from app.contact import contact_routes
from app.database.db import Base, engine
from app.home import home_routes
from app.statement import statement_routes
from app.user import user_routes

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)


def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully.")
    except Exception as exc:
        logger.error("Error initializing the database: %s", exc)


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=PROJECT_NAME,
    version=VERSION,
    description=(
        "Reference API for the dev-challenge lab. "
        "Specs and acceptance criteria live in `specs/`."
    ),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, tags=["authentication"])
app.include_router(home_routes.router, tags=["home"])
app.include_router(user_routes.router, tags=["users"])
app.include_router(statement_routes.router, tags=["statement"])
app.include_router(balance_routes.router, tags=["balance"])
app.include_router(contact_routes.router, tags=["contact"])
