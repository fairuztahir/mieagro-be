prod_category_post_schema = {
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
    'complete_name': {
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
    'parent_id': {
        'required': True,
        'type': ['boolean', 'list'],
    },
    'parent_path': {
        'required': True,
        'type': 'string',
        'empty': False,
        'maxlength': 100
    },
    'child_id': {
        'required': True,
        'type': 'list'
    },
    'product_count': {
        'required': True,
        'type': 'integer',
        'coerce': int,
        'min': 0
    },
    'create_date': {
        'required': True,
        'type': 'string',
        'empty': False,
        'maxlength': 20
    }
}

prod_category_upd_schema = {
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
    'complete_name': {
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
    'parent_id': {
        'required': True,
        'type': ['boolean', 'list'],
    },
    'parent_path': {
        'required': True,
        'type': 'string',
        'empty': False,
        'maxlength': 100
    },
    'child_id': {
        'required': True,
        'type': 'list'
    },
    'product_count': {
        'required': True,
        'type': 'integer',
        'coerce': int,
        'min': 0
    },
    'create_date': {
        'required': True,
        'type': 'string',
        'empty': False,
        'maxlength': 20
    }
}
