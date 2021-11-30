prod_post_schema = {
    'id': {
        'required': True,
        'type': 'integer',
        'coerce': int,
        'min': 1
    },
    'default_code': {
        'required': True,
        'type': ['string', 'boolean'],
        'empty': False,
        'maxlength': 20
    },
    'name': {
        'required': True,
        'type': 'string',
        'empty': False,
        'maxlength': 100
    },
    'display_name': {
        'required': True,
        'type': 'string',
        'empty': False,
        'maxlength': 100
    },
    'active': {
        'required': True,
        'type': 'boolean',
        'empty': False
    },
    'available_in_pos': {
        'required': True,
        'type': 'boolean',
        'empty': False
    },
    'uom_name': {
        'required': True,
        'type': 'string',
        'empty': False,
        'maxlength': 20
    },
    'price': {
        'required': True,
        'type': 'float',
        'coerce': float
    },
    'list_price': {
        'required': True,
        'type': 'float',
        'coerce': float
    },
    'standard_price': {
        'required': True,
        'type': 'float',
        'coerce': float
    },
    'product_variant_count': {
        'required': True,
        'type': 'integer',
        'coerce': int
    },
    'product_variant_ids': {
        'required': True,
        'type': 'list'
    },
    'barcode': {
        'required': True,
        'type': ['string', 'boolean'],
        'empty': False,
        'maxlength': 50
    },
    'qty_available': {
        'required': True,
        'type': 'float',
        'coerce': float
    },
    'incoming_qty': {
        'required': True,
        'type': 'float',
        'coerce': float
    },
    'outgoing_qty': {
        'required': True,
        'type': 'float',
        'coerce': float
    },
    'description': {
        'required': True,
        'type': 'string',
        'empty': True,
        'maxlength': 200
    },
    'create_date': {
        'required': True,
        'type': 'string',
        'empty': False,
        'maxlength': 20
    }
}

prod_upd_schema = {
    'id': {
        'required': False,
        'type': 'integer',
        'coerce': int,
        'min': 1
    },
    'default_code': {
        'required': False,
        'type': ['string', 'boolean'],
        'empty': False,
        'maxlength': 20
    },
    'name': {
        'required': False,
        'type': 'string',
        'empty': False,
        'maxlength': 100
    },
    'display_name': {
        'required': False,
        'type': 'string',
        'empty': False,
        'maxlength': 100
    },
    'active': {
        'required': False,
        'type': 'boolean',
        'empty': False
    },
    'available_in_pos': {
        'required': False,
        'type': 'boolean',
        'empty': False
    },
    'uom_name': {
        'required': False,
        'type': 'string',
        'empty': False,
        'maxlength': 20
    },
    'price': {
        'required': False,
        'type': 'float',
        'coerce': float
    },
    'list_price': {
        'required': False,
        'type': 'float',
        'coerce': float
    },
    'standard_price': {
        'required': False,
        'type': 'float',
        'coerce': float
    },
    'product_variant_count': {
        'required': False,
        'type': 'integer',
        'coerce': int
    },
    'product_variant_ids': {
        'required': False,
        'type': 'list'
    },
    'barcode': {
        'required': False,
        'type': ['string', 'boolean'],
        'empty': False,
        'maxlength': 50
    },
    'qty_available': {
        'required': False,
        'type': 'float',
        'coerce': float
    },
    'incoming_qty': {
        'required': False,
        'type': 'float',
        'coerce': float
    },
    'outgoing_qty': {
        'required': False,
        'type': 'float',
        'coerce': float
    },
    'description': {
        'required': False,
        'type': 'string',
        'empty': False,
        'maxlength': 200
    },
    'create_date': {
        'required': False,
        'type': 'string',
        'empty': False,
        'maxlength': 20
    }
}
