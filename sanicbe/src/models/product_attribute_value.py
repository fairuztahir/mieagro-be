from datetime import datetime
from sqlalchemy import Column, String, DateTime, INTEGER, Boolean, ARRAY
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from sqlalchemy.orm import relationship
from .base import BaseModel


class ProductAttributeValue(BaseModel):
    __tablename__ = "product_attribute_value"
    odoo_id = Column(INTEGER(), index=True)
    name = Column(String(100))
    display_name = Column(String(100))
    ptav_active = Column(Boolean(), default=False)
    product_attribute_value_id = Column(INTEGER(), nullable=True)
    attribute_line_id = Column(INTEGER(), nullable=True)
    price_extra = Column(DOUBLE_PRECISION(
        precision=10, asdecimal=True, decimal_return_scale=4), default=0.0000)
    exclude_for = Column(ARRAY(INTEGER), nullable=True)
    product_tmpl_id = Column(INTEGER(), nullable=True)
    attribute_id = Column(INTEGER(), nullable=True)
    ptav_product_variant_ids = Column(ARRAY(INTEGER), nullable=True)
    is_custom = Column(Boolean(), default=False)
    display_type = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "odoo_id": self.odoo_id,
            "name": self.name,
            "display_name": self.display_name,
            "ptav_active": self.ptav_active,
            "product_attribute_value_id": self.product_attribute_value_id,
            "attribute_line_id": self.attribute_line_id,
            "price_extra": self.price_extra,
            "exclude_for": self.exclude_for,
            "product_tmpl_id": self.product_tmpl_id,
            "attribute_id": self.attribute_id,
            "ptav_product_variant_ids": self.ptav_product_variant_ids,
            "is_custom": self.is_custom,
            "display_type": self.display_type,
            "created_at": self.created_at
        }
