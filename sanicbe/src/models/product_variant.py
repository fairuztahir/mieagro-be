from datetime import datetime
from sqlalchemy import Column, String, DateTime, INTEGER, Boolean, ARRAY
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from sqlalchemy.orm import relationship
from .base import BaseModel


class ProductVariant(BaseModel):
    __tablename__ = "product_variant"
    odoo_id = Column(INTEGER(), index=True)
    name = Column(String(100))
    display_name = Column(String(100))
    code = Column(String(50))
    default_code = Column(String(50))
    description = Column(String(100), nullable=True)
    active = Column(Boolean(), default=False)
    product_tmpl_id = Column(INTEGER(), nullable=True)
    barcode = Column(String(50), nullable=True)
    is_product_variant = Column(Boolean(), default=False)
    available_in_pos = Column(Boolean(), default=False)
    attribute_line_ids = Column(ARRAY(INTEGER), nullable=True)
    price = Column(DOUBLE_PRECISION(
        precision=10, asdecimal=True, decimal_return_scale=4), default=0.0000)
    price_extra = Column(DOUBLE_PRECISION(
        precision=10, asdecimal=True, decimal_return_scale=4), default=0.0000)
    free_qty = Column(DOUBLE_PRECISION(
        precision=10, asdecimal=True, decimal_return_scale=1), default=0.0)
    qty_available = Column(DOUBLE_PRECISION(
        precision=10, asdecimal=True, decimal_return_scale=1), default=0.0)
    incoming_qty = Column(DOUBLE_PRECISION(
        precision=10, asdecimal=True, decimal_return_scale=1), default=0.0)
    outgoing_qty = Column(DOUBLE_PRECISION(
        precision=10, asdecimal=True, decimal_return_scale=1), default=0.0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "odoo_id": self.odoo_id,
            "name": self.name,
            "display_name": self.display_name,
            "code": self.code,
            "default_code": self.default_code,
            "description": self.description,
            "active": self.active,
            "product_tmpl_id": self.product_tmpl_id,
            "barcode": self.barcode,
            "is_product_variant": self.is_product_variant,
            "available_in_pos": self.available_in_pos,
            "attribute_line_ids": self.attribute_line_ids,
            "price": self.price,
            "price_extra": self.price_extra,
            "free_qty": self.free_qty,
            "qty_available": self.qty_available,
            "incoming_qty": self.incoming_qty,
            "outgoing_qty": self.outgoing_qty,
            "created_at": self.created_at
        }
