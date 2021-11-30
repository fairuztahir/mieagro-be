user_post_schema = {
    'first_name': {
        'required': True,
        'type': 'list',
        'schema': {
                'type': 'string',
                'empty': False,
                'maxlength': 30
        }
    },
    'last_name': {
        'required': False,
        'type': 'list',
        'schema': {
                'type': 'string',
                'empty': True,
                'maxlength': 30
        }
    },
    'email': {
        'required': True,
        'type': 'list',
        'schema': {
                'type': 'string',
                'empty': False,
                'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        }
    },
    'challenge': {
        'required': True,
        'type': 'list',
        'schema': {
                'type': 'string',
                'empty': False,
                'maxlength': 60
        }
    },
    'role': {
        'required': False,
        'type': 'list',
        'schema': {
                'type': 'string',
                'empty': False,
                'maxlength': 30
        }
    },
}

user_upd_schema = {
    'first_name': {
        'required': False,
        'type': 'string',
        'empty': False,
        'maxlength': 30
    },
    'last_name': {
        'required': False,
        'type': 'string',
        'empty': True,
        'maxlength': 30
    },
    'email': {
        'required': False,
        'type': 'string',
        'empty': False,
        'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    },
    'challenge': {
        'required': False,
        'type': 'string',
        'empty': False,
        'maxlength': 60
    },
    'role': {
        'required': False,
        'type': 'string',
        'empty': False,
        'maxlength': 30
    },
    'status': {
        'required': False,
        'type': 'boolean',
        'empty': False
    },
}

user_reg_schema = {
    'first_name': {
        'required': True,
        'type': 'string',
        'empty': False,
        'maxlength': 30
    },
    'last_name': {
        'required': False,
        'type': 'string',
        'empty': True,
        'maxlength': 30
    },
    'email': {
        'required': True,
        'type': 'string',
        'empty': False,
        'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    },
    'challenge': {
        'required': True,
        'type': 'string',
        'empty': False,
        'maxlength': 60
    },
    'role': {
        'required': False,
        'type': 'string',
        'empty': False,
        'maxlength': 30
    },
    'x-key': {
        'required': True,
        'type': 'string',
        'empty': False,
        'maxlength': 30
    }
}
