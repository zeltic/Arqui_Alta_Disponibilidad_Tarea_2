from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
# from . import models, schemas, crud, database, services
import models, schemas, crud, database, services

app = FastAPI()

# models.Base.metadata.create_all(bind=database.engine)

@app.on_event("startup")
async def startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)

@app.get("/leyes/", response_model=list[schemas.Ley])
async def read_leyes(skip: int = 0, limit: int = 5, db: AsyncSession = Depends(database.get_db)):
    leyes = await crud.get_leyes(db, skip=skip, limit=limit)
    return leyes

# @app.post("/leyes/", response_model=schemas.Ley)
# async def create_ley(ley: schemas.LeyCreate, db: AsyncSession = Depends(database.get_db)):
#     return await crud.create_ley(db=db, ley=ley)

@app.get("/leyes/{id_norma}", response_model=schemas.LeyDetail)
async def read_ley_detail(id_norma: str, db: AsyncSession = Depends(database.get_db)):
    ley = await crud.get_leyes_detalle(db, id_norma)
    return ley

@app.on_event("startup")
async def update_leyes():
    async with database.db_context() as db:
        leyes = services.fetch_latest_laws()
        for ley in leyes:
            await crud.create_ley(db, ley)
            ley_detalle = services.fetch_law_details(ley.id_norma)
            await crud.create_ley_detalle(db, ley_detalle)