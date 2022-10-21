import json
import os
from collections import UserList
from json import JSONEncoder
from turtle import back

from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import relationship
from sqlalchemy.sql import Insert
from sqlalchemy_serializer import SerializerMixin

from app import app, db


@compiles(Insert, "sqlite")
def suffix_insert(insert, compiler, **kwargs):
    stmt = compiler.visit_insert(insert, **kwargs)
    if insert.dialect_kwargs.get("sqlite_on_conflict_do_nothing"):
        stmt += " ON CONFLICT DO NOTHING"
    return stmt


Insert.argument_for("sqlite", "on_conflict_do_nothing", True)


class Base(db.Model, SerializerMixin):
    """Base class for other models

    Args:
        db (_type_): _description_
        SerializerMixin (_type_): SerializerMixin
    """

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )


class Type(Base):
    """_summary_

    Args:
        Base (_type_): _description_
    """

    __tablename__ = "type"

    # serialize_only = ("name", "description", "values")
    # serialize_rules = ()
    
    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description        

    def __setattr__(self, __name, __value) -> None:
        super().__setattr__(__name, __value)
    
    name = db.Column(db.String(128), unique=True)
    description = db.Column(db.Text)

    # one-to-many collection
    titles = db.relationship("Title", backref="type")
    db.UniqueConstraint(name)


genre_title = Table(
    "genre_title",
    Base.metadata,
    Column("title_id", ForeignKey("title.id"), primary_key=True),
    Column("genre_id", ForeignKey("genre.id"), primary_key=True),
)


class Genre(Base):
    """_summary_

    Args:
        Base (_type_): _description_
    """

    def __init__(self, name=None):
        self.name = name

    name = db.Column(db.String(128), unique=True)


class Title(Base):
    """_summary_

    Args:
        Base (_type_): _description_
    """

    __tablename__ = "title"

    # serialize_only = ("primaryTitle", "primaryTitle")
    # serialize_rules = ()

    def __init__(
        self,
        tconst=None,
        titletype=None,
        primarytitle=None,
        originaltitle=None,
        isadult=None,
        startyear=None,
        endyear=None,
        runtimeminutes=None,
        genres=None,
        type=None
    ):
        self.tconst = tconst
        self.primary_title = primarytitle
        self.original_title = originaltitle
        self.is_adult = isadult
        self.start_year = startyear
        self.end_year = endyear
        self.runtime_minutes = runtimeminutes
        self.titletype = titletype
        self.genres = genres,    
        self.type = type   

    tconst = db.Column(db.String(256))
    primary_title = db.Column(db.String(256))
    original_title = db.Column(db.String(256))
    is_adult = db.Column(db.String(256))
    start_year = db.Column(db.String(256))
    end_year = db.Column(db.String(256))
    runtime_minutes = db.Column(db.String(256))

    type_id = Column(db.Integer, db.ForeignKey("type.id"))
    lst_genres = relationship("Genre", secondary=genre_title)
