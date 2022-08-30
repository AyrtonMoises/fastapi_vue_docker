from sqlalchemy import Column, Integer, String, Boolean
from db.database import Base

metadata = Base.metadata


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    disabled = Column(Boolean, default=False)