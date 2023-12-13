#Creacion de la tabla en la BD
from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True) 
    password = Column (String, nullable=False)
