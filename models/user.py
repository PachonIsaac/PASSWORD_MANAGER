#Creacion de la tabla en la BD
from config.database import Base
from sqlalchemy import Column, Integer, String, Boolean

class User(Base):
    __tablename__ = 'User'
    userID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True) 
    password = Column (String, nullable=False)
    disabled = Column (Boolean, default=False)
