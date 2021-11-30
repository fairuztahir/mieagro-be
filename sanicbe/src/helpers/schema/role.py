role_post_schema = {
    'name': {
        'required': True,
        'type': 'string',
        'empty': False,
        'maxlength': 30
    },
    'desc': {
        'required': False,
        'type': 'string',
        'empty': True,
        'maxlength': 250
    },
}

role_upd_schema = {
    'name': {
        'required': False,
        'type': 'string',
        'empty': False,
        'maxlength': 30
    },
    'desc': {
        'required': False,
        'type': 'string',
        'empty': True,
        'maxlength': 250
    },
}
