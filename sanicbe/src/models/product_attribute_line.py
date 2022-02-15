from datetime import datetime
from sqlalchemy import Column, String, DateTime, INTEGER, Boolean, ARRAY
from sqlalchemy.orm import relationship
from .base import BaseModel


class ProductAttributeLine(BaseModel):
    __tablename__ = "product_attribute_line"
    odoo_id = Column(INTEGER(), index=True)
    display_name = Column(String(100))
    active = Column(Boolean(), default=False)
    product_tmpl_id = Column(INTEGER(), nullable=True)
    attribute_id = Column(INTEGER(), nullable=True)
    value_ids = Column(ARRAY(INTEGER), nullable=True)
    product_template_value_ids = Column(ARRAY(INTEGER), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "odoo_id": self.odoo_id,
            "display_name": self.display_name,
            "active": self.active,
            "product_tmpl_id": self.product_tmpl_id,
            "attribute_id": self.attribute_id,
            "value_ids": self.value_ids,
            "product_template_value_ids": self.product_template_value_ids,
            "created_at": self.created_at
        }
