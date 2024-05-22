from typing import List
from typing import Optional

from sqlalchemy import Column, String, Integer, Identity, Sequence, Float, Boolean, ForeignKey, MetaData
from sqlalchemy.orm import Mapped, relationship, declarative_base

Base_db = declarative_base()

class Categor(Base_db):
    __tablename__ = 'categor'
    id = Column(Integer, Identity(start=100), primary_key=True)
    title = Column(String, index=True, nullable=False)
    num = Column(String, index=True, nullable=True)
    description = Column(String, nullable=True)
    children = relationship("Child", back_populates="staff")

class Staff(Base_db):
    __tablename__ = 'staff'
    id = Column(Integer, Identity(start=10), primary_key=True)
    name = Column(String, index=True, nullable=False)
    categor_id = Column(Integer, ForeignKey('categor.id'))
    parent = relationship("Parent", back_populates="categor")