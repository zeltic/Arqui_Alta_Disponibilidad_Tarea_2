from pydantic import BaseModel
from datetime import date

class LeyBase(BaseModel):
    id_norma: str
    titulo: str
    fecha_publicacion: date
    url: str

class LeyCreate(LeyBase):
    pass

class Ley(LeyBase):
    id: int

    class Config:
        orm_mode = True

class LeyDetailBase(BaseModel):
    id_norma: str
    titulo: str
    fecha_promulgacion: date
    fecha_publicacion: date
    texto: str
    url: str

class LeyDetailCreate(LeyDetailBase):
    pass

class LeyDetail(LeyDetailBase):
    id: int

    class Config:
        orm_mode = True
