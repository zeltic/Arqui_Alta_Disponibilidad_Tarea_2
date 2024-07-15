from sqlalchemy import Column, Integer, String, Date
# from .database import Base
from database import Base

class Ley(Base):
    __tablename__ = "leyes"

    id = Column(Integer, primary_key=True, index=True)
    id_norma = Column(String, unique=True, index=True)
    titulo = Column(String, index=True)
    fecha_publicacion = Column(Date)
    url = Column(String)

class LeyDetail(Base):
    __tablename__ = "leyes_detalle"

    id = Column(Integer, primary_key=True, index=True)
    id_norma = Column(String, unique=True, index=True)
    titulo = Column(String, index=True)
    fecha_publicacion = Column(Date)
    fecha_promulgacion = Column(Date)
    texto = Column(String)
    url = Column(String)