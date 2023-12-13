from config.database import Base
from models.user import User
from sqlalchemy import Column, Integer, String, DateTime, event, ForeignKey
from datetime import datetime


class Password(Base):
    __tablename__ = 'Passwords'
    id = Column(Integer, primary_key=True)
    length = Column(Integer, nullable=False) 
    special_characters = Column(Integer, nullable=False)
    numbers = Column(Integer, nullable=False)
    capital_letters = Column(Integer, nullable=False)
    creation_password = Column(DateTime,default= datetime.now())
    password = Column(String)
    id_user = Column(Integer, ForeignKey(User.id))
