wh_post_schema = {
    'id': {
        'required': True,
        'type': 'integer',
        'coerce': int,
        'min': 1
    },
    'code': {
        'required': True,
        'type': 'string',
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
    'reception_steps': {
        'required': False,
        'type': 'string',
        'empty': False,
        'maxlength': 20
    },
    'delivery_steps': {
        'required': False,
        'type': 'string',
        'empty': False,
        'maxlength': 20
    },
    'create_date': {
        'required': True,
        'type': 'string',
        'empty': False,
        'maxlength': 20
    }
}

wh_upd_schema = {
    'id': {
        'required': False,
        'type': 'integer',
        'empty': False,
        'coerce': int,
        'min': 1
    },
    'code': {
        'required': False,
        'type': 'string',
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
    'reception_steps': {
        'required': False,
        'type': 'string',
        'empty': False,
        'maxlength': 20
    },
    'delivery_steps': {
        'required': False,
        'type': 'string',
        'empty': False,
        'maxlength': 20
    },
    'create_date': {
        'required': False,
        'type': 'string',
        'empty': False,
        'maxlength': 20
    }
}
