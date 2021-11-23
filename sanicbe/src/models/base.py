from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

import uuid

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    # MARK: primary ket with uuid
    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)

    # MARK: primary key with integer
    # id = Column(INTEGER(), primary_key=True, index=True)
