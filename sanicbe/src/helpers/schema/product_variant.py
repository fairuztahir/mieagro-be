prod_variant_post_schema = {
    'id': {
        'required': True,
        'type': 'integer',
        'coerce': int,
        'min': 1
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
    'code': {
        'required': True,
        'type': 'string',
        'empty': False,
        'maxlength': 50
    },
    'default_code': {
        'required': True,
        'type': 'string',
        'empty': False,
        'maxlength': 50
    },
    'description': {
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
    'product_tmpl_id': {
        'required': True,
        'type': 'list'
    },
    'barcode': {
        'required': True,
        'type': ['string', 'boolean'],
        'empty': False,
        'maxlength': 50
    },
    'is_product_variant': {
        'required': True,
        'type': 'boolean',
        'empty': False
    },
    'available_in_pos': {
        'required': True,
        'type': 'boolean',
        'empty': False
    },
    'attribute_line_ids': {
        'required': True,
        'type': 'list'
    },
    'price': {
        'required': True,
        'type': 'float'
    },
    'price_extra': {
        'required': True,
        'type': 'float'
    },
    'free_qty': {
        'required': True,
        'type': 'float'
    },
    'qty_available': {
        'required': True,
        'type': 'float'
    },
    'incoming_qty': {
        'required': True,
        'type': 'float'
    },
    'outgoing_qty': {
        'required': True,
        'type': 'float'
    },
    'create_date': {
        'required': True,
        'type': 'string',
        'empty': False,
        'maxlength': 20
    }
}

prod_variant_upd_schema = {
    'id': {
        'required': True,
        'type': 'integer',
        'coerce': int,
        'min': 1
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
    'code': {
        'required': True,
        'type': 'string',
        'empty': False,
        'maxlength': 50
    },
    'default_code': {
        'required': True,
        'type': 'string',
        'empty': False,
        'maxlength': 50
    },
    'description': {
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
    'product_tmpl_id': {
        'required': True,
        'type': 'list'
    },
    'barcode': {
        'required': True,
        'type': ['string', 'boolean'],
        'empty': False,
        'maxlength': 50
    },
    'is_product_variant': {
        'required': True,
        'type': 'boolean',
        'empty': False
    },
    'available_in_pos': {
        'required': True,
        'type': 'boolean',
        'empty': False
    },
    'attribute_line_ids': {
        'required': True,
        'type': 'list'
    },
    'price': {
        'required': True,
        'type': 'float'
    },
    'price_extra': {
        'required': True,
        'type': 'float'
    },
    'free_qty': {
        'required': True,
        'type': 'float'
    },
    'qty_available': {
        'required': True,
        'type': 'float'
    },
    'incoming_qty': {
        'required': True,
        'type': 'float'
    },
    'outgoing_qty': {
        'required': True,
        'type': 'float'
    },
    'create_date': {
        'required': True,
        'type': 'string',
        'empty': False,
        'maxlength': 20
    }
}
