from sqlalchemy import create_engine, Column, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, DateTime, Text
from scrapy.utils.project import get_project_settings

Base = declarative_base()

metadata = MetaData()


def db_connect():
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(bind=engine)


class Story(Base):
    __tablename__ = "story"

    id = Column(Integer, ForeignKey("meta.id"), primary_key=True)
    title = Column("title", String(200), nullable=False)
    text = Column("text", Text())

    meta = relationship("Meta", backref="story")


class Meta(Base):
    __tablename__ = "meta"

    id = Column(Integer, primary_key=True)
    link = Column("link", String(200), unique=True, nullable=False)
    date = Column("date", DateTime, nullable=False)
    author_id = Column(Integer, ForeignKey("author.id"))


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    name = Column("name", String(100), unique=True, nullable=False)
    link = Column("link", String(200), unique=True, nullable=False)

    works = relationship("Meta", backref="author")
