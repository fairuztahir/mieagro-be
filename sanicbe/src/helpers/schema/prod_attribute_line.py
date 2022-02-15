prod_attr_line_post_schema = {
    'id': {
        'required': True,
        'type': 'integer',
        'coerce': int,
        'min': 1
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
    'product_tmpl_id': {
        'required': True,
        'type': 'list'
    },
    'attribute_id': {
        'required': True,
        'type': 'list'
    },
    'value_ids': {
        'required': True,
        'type': 'list'
    },
    'product_template_value_ids': {
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

prod_attr_line_upd_schema = {
    'id': {
        'required': True,
        'type': 'integer',
        'coerce': int,
        'min': 1
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
    'product_tmpl_id': {
        'required': True,
        'type': 'list'
    },
    'attribute_id': {
        'required': True,
        'type': 'list'
    },
    'value_ids': {
        'required': True,
        'type': 'list'
    },
    'product_template_value_ids': {
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
