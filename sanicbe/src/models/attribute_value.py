from datetime import datetime
from sqlalchemy import Column, String, DateTime, INTEGER, Boolean, ARRAY
from sqlalchemy.orm import relationship
from .base import BaseModel


class AttributeValue(BaseModel):
    __tablename__ = "attribute_values"
    odoo_id = Column(INTEGER(), index=True)
    name = Column(String(100))
    display_name = Column(String(100))
    attribute_id = Column(INTEGER(), nullable=True)
    pav_attribute_line_ids = Column(ARRAY(INTEGER), nullable=True)
    is_used_on_products = Column(Boolean(), default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "odoo_id": self.odoo_id,
            "name": self.name,
            "display_name": self.display_name,
            "attribute_id": self.attribute_id,
            "pav_attribute_line_ids": self.pav_attribute_line_ids,
            "is_used_on_products": self.is_used_on_products,
            "created_at": self.created_at
        }
