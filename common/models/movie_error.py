# coding: utf-8
from sqlalchemy import Column, Integer, MetaData, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.ext.declarative import declarative_base
from application import db

Base = declarative_base()
metadata = Base.metadata



class MovieError(db.Model):
    __tablename__ = 'movie_error'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, server_default=FetchedValue(), info='电影名称')
    url = Column(String(300), nullable=False, server_default=FetchedValue(), info='电影详情地址')
    remarks = Column(String(2048), nullable=False, server_default=FetchedValue(), info='备注')

    def __init__(self, **kwargs):
        for key in kwargs:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])


