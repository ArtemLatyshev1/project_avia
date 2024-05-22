from typing import Union, Annotated
from pydantic import BaseModel, Field, HttpUrl
from sqlalchemy import Column, String, Integer, Identity, Sequence, Float, Boolean, ForeignKey, MetaData
from sqlalchemy.orm import declarative_base
from enum import Enum

Base = declarative_base()
# metadata = MetaData()
# class User_DB(metadata):
#     __tablename__ = "users"
#     id = Column(Integer, Sequence("user_id_seq", start=1), primary_key=True)
#     name = Column(String, index=True, nullable=False)
#     folder = Column(String, nullable=True)
#     hashed_password = Column(String)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Identity(start=10), primary_key=True)
    name = Column(String, index=True, nullable=False)
    hashed_password = Column(String)

    # goods = relationship("Good", back_populates="owner")

# class Good(metadata):
#     __tablename__ = "goods"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     description = Column(String, index=True)
#     price = Column(Float)
#     nalog = Column(Float)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     owner = relationship("User", back_populates="goods")
class Tags(Enum):
    users = "users"
    advents = "advents"
    info = "info"
    good = "good"


class Person(BaseModel):
    lastName: str = Field(default="lastname", min_length=3, max_length=20)
    age: int = Field(default=100, ge=10, lt=200)


class Foto(BaseModel):
    url: HttpUrl
    name: Union[str, None] = None


class User_new(BaseModel):
    name: Union[str, None] = None
    id: Annotated[Union[int, None], Field(default=100, ge=10, lt=200)] = None
    person: Union[Person, None] = None
    day_list0: list
    day_list1: Union[list, None] = None
    day_list2: Union[list[int], None] = None
    foto_list: Union[list[Foto], None] = None


class Good(BaseModel):
    id: Annotated[Union[int, None], Field(default=100, ge=1, lt=200)] = None
    name: Union[str, None] = None
    description: Union[str, None] = None
    price: Union[float, None] = 0
    nalog: Union[float, None] = 13.6


class Main_User(BaseModel):
    id: Annotated[Union[int, None], Field(default=100, ge=1, lt=200)] = None
    name: Union[str, None] = None


class Main_UserDB(Main_User):
    hashed_password: Annotated[Union[str, None], Field(max_length=200, min_length=6)] = None


class New_Respons(BaseModel):
    message: str