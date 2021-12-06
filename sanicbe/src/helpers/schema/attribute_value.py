attr_value_post_schema = {
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
    'attribute_id': {
        'required': True,
        'type': 'list'
    },
    'pav_attribute_line_ids': {
        'required': True,
        'type': 'list'
    },
    'is_used_on_products': {
        'required': True,
        'type': 'boolean',
        'empty': False
    },
    'create_date': {
        'required': True,
        'type': 'string',
        'empty': False,
        'maxlength': 20
    }
}

attr_value_upd_schema = {
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
    'attribute_id': {
        'required': True,
        'type': 'list'
    },
    'pav_attribute_line_ids': {
        'required': True,
        'type': 'list'
    },
    'is_used_on_products': {
        'required': True,
        'type': 'boolean',
        'empty': False
    },
    'create_date': {
        'required': True,
        'type': 'string',
        'empty': False,
        'maxlength': 20
    }
}
