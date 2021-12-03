from datetime import datetime
from sqlalchemy import Column, String, DateTime, INTEGER, Boolean, ARRAY
from sqlalchemy.orm import relationship
from .base import BaseModel


class Attribute(BaseModel):
    __tablename__ = "attributes"
    odoo_id = Column(INTEGER(), index=True)
    name = Column(String(100))
    display_name = Column(String(100))
    value_ids = Column(ARRAY(INTEGER), nullable=True)
    attribute_line_ids = Column(ARRAY(INTEGER), nullable=True)
    is_used_on_products = Column(Boolean(), default=False)
    product_tmpl_ids = Column(ARRAY(INTEGER), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "odoo_id": self.odoo_id,
            "name": self.name,
            "display_name": self.display_name,
            "value_ids": self.value_ids,
            "attribute_line_ids": self.attribute_line_ids,
            "is_used_on_products": self.is_used_on_products,
            "product_tmpl_ids": self.product_tmpl_ids,
            "created_at": self.created_at
        }
