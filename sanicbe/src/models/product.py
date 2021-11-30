from datetime import datetime
from sqlalchemy import Column, String, DateTime, INTEGER, Boolean, Float, ARRAY
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from sqlalchemy.orm import relationship
from .base import BaseModel


class Product(BaseModel):
    __tablename__ = "products"
    odoo_id = Column(INTEGER(), index=True)
    code = Column(String(20))
    name = Column(String(100))
    display_name = Column(String(150))
    active = Column(Boolean(), default=False)
    available_in_pos = Column(Boolean(), default=False)
    uom_name = Column(String(20), default='Units')
    template_price = Column(DOUBLE_PRECISION(
        precision=10, asdecimal=True, decimal_return_scale=4), default=0.0000)
    template_list_price = Column(DOUBLE_PRECISION(
        precision=10, asdecimal=True, decimal_return_scale=4), default=0.0000)
    template_cost_price = Column(DOUBLE_PRECISION(
        precision=10, asdecimal=True, decimal_return_scale=4), default=0.0000)
    product_variant_count = Column(INTEGER(), nullable=True)
    product_variant_ids = Column(ARRAY(INTEGER), nullable=True)
    barcode = Column(String(50), nullable=True)
    qty_available = Column(DOUBLE_PRECISION(
        precision=10, asdecimal=True, decimal_return_scale=1), default=0.0)
    incoming_qty = Column(DOUBLE_PRECISION(
        precision=10, asdecimal=True, decimal_return_scale=1), default=0.0)
    outgoing_qty = Column(DOUBLE_PRECISION(
        precision=10, asdecimal=True, decimal_return_scale=1), default=0.0)
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
            "uom_name": self.uom_name,
            "template_price": self.template_price,
            "template_list_price": self.template_list_price,
            "template_cost_price": self.template_cost_price,
            "product_variant_count": self.product_variant_count,
            "product_variant_ids": self.product_variant_ids,
            "barcode": self.barcode,
            "qty_available": self.qty_available,
            "incoming_qty": self.incoming_qty,
            "outgoing_qty": self.outgoing_qty,
            "description": self.description,
            "created_at": self.created_at
        }
