from cerberus import Validator
from .schema.product import prod_post_schema, prod_upd_schema
from .schema.warehouse import wh_post_schema, wh_upd_schema
from .schema.role import role_post_schema, role_upd_schema
from .schema.user import user_post_schema, user_upd_schema, user_reg_schema, users_post_schema
from .schema.attribute import attr_post_schema, attr_upd_schema
from .schema.attribute_value import attr_value_post_schema, attr_value_upd_schema
from .schema.prod_attribute_line import prod_attr_line_post_schema, prod_attr_line_upd_schema
from .schema.prod_attribute_value import prod_attr_value_post_schema, prod_attr_value_upd_schema
from .schema.product_variant import prod_variant_post_schema, prod_variant_upd_schema
from .schema.product_category import prod_category_post_schema, prod_category_upd_schema


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


# default main validator
def nestedValidator(schema={}, document={}):
    v = Validator()
    v.allow_unknown = True

    if not v.validate(document, schema):
        arr = []
        for _, value in v.errors.items():
            for k, v in value[0].items():
                tmp = {}
                for c, d in v[0].items():
                    tmp['data_row'] = k
                    tmp[c] = d[0]
                arr.append(tmp)
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
            'type': 'list'
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

    # 'sortParam': {
    #     'required': False,
    #     'type': 'list',
    #     'schema': {
    #         'type': 'string',
    #         'allowed': ['id', 'name', 'created_at']
    #     }
    # },

    return mainValidator(schema, input)


# Post role validator
def postRoleValidator(input={}):
    return mainValidator(role_post_schema, input)


# Update role validator
def updateRoleValidator(input={}):
    return mainValidator(role_upd_schema, input)


# Post user validator
def postUserValidator(input={}):
    return mainValidator(user_post_schema, input)


# Post users validator
def postUsersValidator(input={}):
    return nestedValidator(users_post_schema, input)


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


# Post attribute validator
def postAttributeValidator(input=[]):
    flag_ = True
    err_list = []
    for i in range(len(input)):
        [result, err] = mainValidator(attr_post_schema, input[i])
        if not result:
            flag_ = False
            err['id'] = input[i]['id']
            err_list.append(err)

    return [flag_, err_list]


# Update attribute validator
def updateAttributeValidator(input={}):
    return mainValidator(attr_upd_schema, input)


# Post attribute value validator
def postAttributeValueValidator(input=[]):
    flag_ = True
    err_list = []
    for i in range(len(input)):
        [result, err] = mainValidator(attr_value_post_schema, input[i])
        if not result:
            flag_ = False
            err['id'] = input[i]['id']
            err_list.append(err)

    return [flag_, err_list]


# Update attribute value validator
def updateAttributeValueValidator(input={}):
    return mainValidator(attr_value_upd_schema, input)


# Post prod attribute line validator
def postProdAttributeLineValidator(input=[]):
    flag_ = True
    err_list = []
    for i in range(len(input)):
        [result, err] = mainValidator(prod_attr_line_post_schema, input[i])
        if not result:
            flag_ = False
            err['id'] = input[i]['id']
            err_list.append(err)

    return [flag_, err_list]


# Update prod attribute line validator
def updateProdAttributeLineValidator(input={}):
    return mainValidator(prod_attr_line_upd_schema, input)


# Post prod attribute value validator
def postProdAttributeValueValidator(input=[]):
    flag_ = True
    err_list = []
    for i in range(len(input)):
        [result, err] = mainValidator(prod_attr_value_post_schema, input[i])
        if not result:
            flag_ = False
            err['id'] = input[i]['id']
            err_list.append(err)

    return [flag_, err_list]


# Update prod attribute value validator
def updateProdAttributeValueValidator(input={}):
    return mainValidator(prod_attr_value_upd_schema, input)


# Post prod variant validator
def postProdVariantValidator(input=[]):
    flag_ = True
    err_list = []
    for i in range(len(input)):
        [result, err] = mainValidator(prod_variant_post_schema, input[i])
        if not result:
            flag_ = False
            err['id'] = input[i]['id']
            err_list.append(err)

    return [flag_, err_list]


# Update prod variant validator
def updateProdVariantValidator(input={}):
    return mainValidator(prod_variant_upd_schema, input)


# Post prod category validator
def postProdCategoryValidator(input=[]):
    flag_ = True
    err_list = []
    for i in range(len(input)):
        [result, err] = mainValidator(prod_category_post_schema, input[i])
        if not result:
            flag_ = False
            err['id'] = input[i]['id']
            err_list.append(err)

    return [flag_, err_list]


# Update prod category validator
def updateProdCategoryValidator(input={}):
    return mainValidator(prod_category_upd_schema, input)
