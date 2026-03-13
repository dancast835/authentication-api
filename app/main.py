from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database.db import create_db_and_tables
from app.routes.routes import router


#new way to implement the on_startup feature for fastapi
@asynccontextmanager
async def lifespan(app: FastAPI):
    #startup
    create_db_and_tables()
    yield



app = FastAPI(
    title="Authentication API",
    version="1.0.0",
    description="Phase 1 authentication backend using FastAPI, SQLModel, and JWT",
    lifespan=lifespan
)

app.include_router(router)
