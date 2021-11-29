from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from .base import BaseModel


class Role(BaseModel):
    __tablename__ = "roles"
    name = Column(String(20))
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)
    users = relationship("User")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description, "created_at": self.created_at}

    def relation_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description, "users": [{"id": user.id, "name": user.fname + ' ' + user.lname} for user in self.users]}
