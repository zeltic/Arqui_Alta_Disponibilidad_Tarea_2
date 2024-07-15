from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
# from . import models, schemas
import models, schemas
import logging

async def get_leyes(db: AsyncSession, skip: int = 0, limit: int = 5):
    result = await db.execute(select(models.Ley).offset(skip).limit(limit))
    return result.scalars().all()

async def create_ley(db: AsyncSession, ley: schemas.LeyCreate):
    db_ley = models.Ley(**ley.dict())
    db.add(db_ley)
    await db.commit()
    await db.refresh(db_ley)
    return db_ley

async def get_leyes_detalle(db: AsyncSession, id_norma: str):
    result = await db.execute(select(models.LeyDetail).filter(models.LeyDetail.id_norma == id_norma))
    db_ley = result.scalars().first()
    # logger = logging.getLogger('uvicorn.error')
    # logger.setLevel(logging.DEBUG)
    # logger.debug(ley)
    return db_ley

async def create_ley_detalle(db: AsyncSession, ley: schemas.LeyDetailCreate):
    db_ley = models.LeyDetail(**ley.dict())
    db.add(db_ley)
    await db.commit()
    await db.refresh(db_ley)
    return db_ley