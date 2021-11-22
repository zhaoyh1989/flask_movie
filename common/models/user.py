# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.ext.declarative import declarative_base
from application import db

Base = declarative_base()
metadata = Base.metadata



class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, info='主键')
    nickname = Column(String(30), nullable=False, info='昵称')
    login_name = Column(String(20), nullable=False, unique=True, info='登录用户名')
    login_pwd = Column(String(32), nullable=False, info='登录密码')
    login_salt = Column(String(32), nullable=False, info='登录密码随机码')
    status = Column(Integer, nullable=False, server_default=FetchedValue(), info='状态 0：无效；1：有效')
    updated_time = Column(DateTime, nullable=False, server_default=FetchedValue(), info='最后更新时间')
    created_time = Column(DateTime, nullable=False, server_default=FetchedValue(), info='创建时间')
    remarks = Column(String(512))
