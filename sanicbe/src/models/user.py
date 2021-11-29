from datetime import datetime
from sqlalchemy import Column, ForeignKey, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    fname = Column(String(20), nullable=False)
    lname = Column(String(20), nullable=True)
    email = Column(String(100), nullable=False, index=True)
    challenge = Column(String(), nullable=False)
    role_id = Column(ForeignKey("roles.id"))
    avatar_url = Column(String(), nullable=True)
    status = Column(Boolean(), nullable=False, default=False)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)
    role = relationship("Role", back_populates="users")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.fname + ' ' + self.lname,
            "email": self.email,
            "challenge": self.challenge,
            "avatar_url": self.avatar_url,
            "status": self.status,
            "last_login": self.last_login,
            "created_at": self.created_at,
            "role": {"name": self.role.name}
        }
