from sqlalchemy import Column, String,Integer,DateTime
from sqlalchemy.ext.declarative import declarative_base
Base=declarative_base()
class token(Base):
    __tablename__='token'
    username=Column(String(30),primary_key=True)
    token=Column(String(32))
class contacts(Base):
    __tablename__='contacts'
    id=Column(Integer,primary_key=True)
    group_name=Column(String(30))
    username=Column(String(30))
    contact_name=Column(String(20))
    contact=Column(String(30))
    type=Column(String(5))
class user(Base):
    __tablename__='user'
    username=Column(String(30),primary_key=True)
    password=Column(String(100))
    phone=Column(String(11))
class contacts_group(Base):
    __tablename__='contacts_group'
    id=Column(Integer,primary_key=True)
    username=Column(String(30))
    group_name=Column(String(30))
class task(Base):
    __tablename__='task'
    id=Column(Integer,primary_key=True)
    username=Column(String(30))
    task=Column(String(100))
    send_list=Column(String(255))
    set_date=Column(String(20))
    send_way=Column(String(4))
    status=Column(String(10))

