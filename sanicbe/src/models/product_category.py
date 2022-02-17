from datetime import datetime
from sqlalchemy import Column, String, DateTime, INTEGER, Boolean, ARRAY
from sqlalchemy.orm import relationship
from .base import BaseModel


class ProductCategory(BaseModel):
    __tablename__ = "product_category"
    odoo_id = Column(INTEGER(), index=True)
    name = Column(String(100))
    complete_name = Column(String(100))
    display_name = Column(String(100))
    parent_id = Column(INTEGER(), nullable=True)
    parent_path = Column(String(100))
    child_id = Column(ARRAY(INTEGER), nullable=True)
    product_count = Column(INTEGER(), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "odoo_id": self.odoo_id,
            "name": self.name,
            "complete_name": self.complete_name,
            "display_name": self.display_name,
            "parent_id": self.parent_id,
            "parent_path": self.parent_path,
            "child_id": self.child_id,
            "product_count": self.product_count,
            "created_at": self.created_at
        }
