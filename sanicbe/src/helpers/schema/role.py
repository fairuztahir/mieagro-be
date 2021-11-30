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
        'maxlength': 250
    },
}
