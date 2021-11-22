# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, MetaData, String, Text
from sqlalchemy.schema import FetchedValue
from sqlalchemy.ext.declarative import declarative_base
from application import db


Base = declarative_base()
metadata = Base.metadata



class Movie(db.Model):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, server_default=FetchedValue(), info='电影名称')
    classify = Column(String(100), nullable=False, server_default=FetchedValue(), info='类别')
    actor = Column(String(2000), nullable=False, server_default=FetchedValue(), info='主演')
    cover_pic = Column(String(300), nullable=False, server_default=FetchedValue(), info='封面图')
    pics = Column(String(1000), nullable=False, server_default=FetchedValue(), info='图片地址json')
    url = Column(String(300), nullable=False, server_default=FetchedValue(), info='电影详情地址')
    desc = Column(Text, nullable=False, info='电影描述')
    magnet_url = Column(String(5000), nullable=False, server_default=FetchedValue(), info='磁力下载地址')
    hash = Column(String(64), nullable=False, unique=True, server_default=FetchedValue(), info='唯一值')
    pub_date = Column(String(512), nullable=False, index=True, server_default=FetchedValue(), info='发布日期')
    source = Column(String(20), nullable=False, server_default=FetchedValue(), info='来源')
    view_counter = Column(Integer, nullable=False, server_default=FetchedValue(), info='阅读数量')
    updated_time = Column(DateTime, nullable=False, server_default=FetchedValue(), info='最后更新时间')
    created_time = Column(DateTime, nullable=False, server_default=FetchedValue(), info='插入时间')

    def __init__(self, **kwargs):
        for key in kwargs:
            if hasattr(self,key):
                setattr(self,key,kwargs[key])
