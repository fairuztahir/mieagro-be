from datetime import datetime
from sqlalchemy import Column, String, DateTime, INTEGER, Boolean
from sqlalchemy.orm import relationship
from .base import BaseModel


class Warehouse(BaseModel):
    __tablename__ = "warehouses"
    odoo_id = Column(INTEGER(), index=True)
    code = Column(String(20))
    name = Column(String(100))
    display_name = Column(String(100))
    active = Column(Boolean(), default=False)
    reception_steps = Column(String(20), default='one_step')
    delivery_steps = Column(String(20), default='ship_only')
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "odoo_id": self.odoo_id,
            "code": self.code,
            "name": self.name,
            "display_name": self.display_name,
            "active": self.active,
            "reception_steps": self.reception_steps,
            "delivery_steps": self.delivery_steps,
            "description": self.description,
            "created_at": self.created_at
        }
