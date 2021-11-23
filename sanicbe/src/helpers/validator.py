from cerberus import Validator


# default main validator
def mainValidator(schema={}, document={}):
    v = Validator()
    v.allow_unknown = True

    if not v.validate(document, schema):
        arr = {}
        for key, value in v.errors.items():
            if key == 'email':
                arr[key] = 'Invalid email address'
            elif isinstance(value[0][0], list):
                arr[key] = value[0][0][0]
            else:
                arr[key] = value[0]
        return [False, arr]
    else:
        return [True, None]


# Pagination validation
def paginateValidator(input={}):
    schema = {
        'pageSize': {
            'required': True,
            'type': 'list',
            'schema': {
                'type': 'integer',
                'coerce': int,
                'min': 5,
                'max': 100
            }
        },
        'page': {
            'required': True,
            'type': 'list',
            'schema': {
                'type': 'integer',
                'coerce': int,
                'min': 1
            }
        },
        'sortParam': {
            'required': False,
            'type': 'list',
            'schema': {
                'type': 'string',
                'allowed': ['id', 'name', 'created_at']
            }
        },
        'sortBy': {
            'required': False,
            'type': 'list',
            'schema': {
                'type': 'string',
                'allowed': ['desc', 'asc', 'DESC', 'ASC']
            }
        }
    }

    return mainValidator(schema, input)


# Post role validator
def postRoleValidator(input={}):
    schema = {
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
    return mainValidator(schema, input)


# Post user validator
def postUserValidator(input={}):
    schema = {
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
    return mainValidator(schema, input)


# Register user validator
def registerUserValidator(input={}):
    schema = {
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
    return mainValidator(schema, input)


# Update user validator
def updateUserValidator(input={}):
    schema = {
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
    return mainValidator(schema, input)
