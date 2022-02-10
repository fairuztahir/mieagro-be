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
                'regex': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
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
        'regex': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
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
        'regex': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
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

users_post_schema = {
    'data': {
        'type': 'list',
        'required': True,
        'schema': {
            'type': 'dict',
            'schema': {
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
                    'regex': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
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
            }
        },
    },
}
