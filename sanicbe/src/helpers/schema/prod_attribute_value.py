prod_attr_value_post_schema = {
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
    'ptav_active': {
        'required': True,
        'type': 'boolean',
        'empty': False
    },
    'product_attribute_value_id': {
        'required': True,
        'type': 'list'
    },
    'attribute_line_id': {
        'required': True,
        'type': 'list'
    },
    'price_extra': {
        'required': True,
        'type': 'float'
    },
    'exclude_for': {
        'required': True,
        'type': 'list'
    },
    'product_tmpl_id': {
        'required': True,
        'type': 'list'
    },
    'attribute_id': {
        'required': True,
        'type': 'list'
    },
    'ptav_product_variant_ids': {
        'required': True,
        'type': 'list'
    },
    'is_custom': {
        'required': True,
        'type': 'boolean',
        'empty': False
    },
    'display_type': {
        'required': True,
        'type': 'string',
        'empty': False,
        'maxlength': 100
    },
    'create_date': {
        'required': True,
        'type': 'string',
        'empty': False,
        'maxlength': 20
    }
}

prod_attr_value_upd_schema = {
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
    'ptav_active': {
        'required': True,
        'type': 'boolean',
        'empty': False
    },
    'product_attribute_value_id': {
        'required': True,
        'type': 'list'
    },
    'attribute_line_id': {
        'required': True,
        'type': 'list'
    },
    'price_extra': {
        'required': True,
        'type': 'float'
    },
    'exclude_for': {
        'required': True,
        'type': 'list'
    },
    'product_tmpl_id': {
        'required': True,
        'type': 'list'
    },
    'attribute_id': {
        'required': True,
        'type': 'list'
    },
    'ptav_product_variant_ids': {
        'required': True,
        'type': 'list'
    },
    'is_custom': {
        'required': True,
        'type': 'boolean',
        'empty': False
    },
    'display_type': {
        'required': True,
        'type': 'string',
        'empty': False,
        'maxlength': 100
    },
    'create_date': {
        'required': True,
        'type': 'string',
        'empty': False,
        'maxlength': 20
    }
}
