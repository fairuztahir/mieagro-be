from sqlalchemy import INTEGER, Column
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = Column(INTEGER(), primary_key=True, index=True)
