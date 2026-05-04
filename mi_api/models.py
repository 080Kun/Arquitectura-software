from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class Item(Base):
    __tablename__ = "coches"

    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String, nullable=True)
    modelo = Column(String, nullable=True)
    matricula = Column(String, nullable=True)
