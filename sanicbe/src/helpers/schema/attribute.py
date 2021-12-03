attr_post_schema = {
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
    'value_ids': {
        'required': True,
        'type': 'list'
    },
    'attribute_line_ids': {
        'required': True,
        'type': 'list'
    },
    'is_used_on_products': {
        'required': True,
        'type': 'boolean',
        'empty': False
    },
    'product_tmpl_ids': {
        'required': True,
        'type': 'list'
    },
    'create_date': {
        'required': True,
        'type': 'string',
        'empty': False,
        'maxlength': 20
    }
}

attr_upd_schema = {
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
    'value_ids': {
        'required': True,
        'type': 'list'
    },
    'attribute_line_ids': {
        'required': True,
        'type': 'list'
    },
    'is_used_on_products': {
        'required': True,
        'type': 'boolean',
        'empty': False
    },
    'product_tmpl_ids': {
        'required': True,
        'type': 'list'
    },
    'create_date': {
        'required': True,
        'type': 'string',
        'empty': False,
        'maxlength': 20
    }
}
