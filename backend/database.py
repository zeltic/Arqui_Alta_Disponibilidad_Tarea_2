from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager, contextmanager
from os import environ as env

# Cambia esto con tu configuración de PostgreSQL
# DATABASE_URL = "postgresql+asyncpg://username:password@localhost/dbname"
DATABASE_URL = f"postgresql+asyncpg://{env['DATABASE_USERNAME']}:{env['DATABASE_PASSWORD']}@{env['DATABASE_HOST']}:{env['DATABASE_PORT']}/{env['DATABASE_NAME']}"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

Base = declarative_base()

# @asynccontextmanager
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

@asynccontextmanager
async def db_context():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# db_context = contextmanager(get_db)

# async def get_db():
#     async with SessionLocal() as session:
#         yield session