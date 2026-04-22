from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy import String, Text, Table, ForeignKey, Column, Integer, inspect, select, desc, func
from sqlalchemy.ext.hybrid import hybrid_property
import uuid
#from .common import *
from .engine import *

class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    @classmethod
    def session(cls):
        return SessionLocal()

    @property
    def persistent(self):
        return inspect(self).persistent