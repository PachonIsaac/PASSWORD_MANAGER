from config.database import Base
from models.user import User
from sqlalchemy import Column, Integer, String, DateTime, event, ForeignKey
from datetime import datetime


class Password(Base):
    __tablename__ = 'Passwords'
    passwordID = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey(User.userID))
    creation_password = Column(DateTime,default= datetime.now())
    password = Column(String)
    
