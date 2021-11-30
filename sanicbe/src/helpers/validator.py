from cerberus import Validator
from .schema.product import prod_post_schema, prod_upd_schema
from .schema.warehouse import wh_post_schema, wh_upd_schema
from .schema.role import role_post_schema
from .schema.user import user_post_schema, user_upd_schema, user_reg_schema


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
    return mainValidator(role_post_schema, input)


# Post user validator
def postUserValidator(input={}):
    return mainValidator(user_post_schema, input)


# Register user validator
def registerUserValidator(input={}):
    return mainValidator(user_reg_schema, input)


# Update user validator
def updateUserValidator(input={}):
    return mainValidator(user_upd_schema, input)


# Post warehouse validator
def postWarehouseValidator(input=[]):
    flag_ = True
    err_list = []
    for i in range(len(input)):
        [result, err] = mainValidator(wh_post_schema, input[i])
        if not result:
            flag_ = False
            err['id'] = input[i]['id']
            err_list.append(err)

    return [flag_, err_list]


# Update warehouse validator
def updateWarehouseValidator(input={}):
    return mainValidator(wh_upd_schema, input)


# Post product validator
def postProductValidator(input=[]):
    flag_ = True
    err_list = []
    for i in range(len(input)):
        [result, err] = mainValidator(prod_post_schema, input[i])
        if not result:
            flag_ = False
            err['id'] = input[i]['id']
            err_list.append(err)

    return [flag_, err_list]


# Update product validator
def updateProductValidator(input={}):
    return mainValidator(prod_upd_schema, input)
