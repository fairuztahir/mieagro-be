from helpers.func import (
    resJson,
    resType,
    exceptionRaise,
    validate_list
)
from helpers.validator import paginateValidator, postAttributeValidator, updateAttributeValidator
from helpers.query import (
    paginatedQuery,
    insertQuery,
    softDelbyId,
    findRecordById,
    findRecordByColumn,
    findRecordByColumnCron,
    updateById
)
from sanic.log import logger
from sanic import Blueprint
from models.attribute import Attribute
from utils.auth import protected
from sqlalchemy import update
from odoo.main import get_attr

import arrow

# -----------------
# API Class Section
# -----------------


class AttributeController():
    p = Blueprint('attribute', url_prefix='/')

    @p.get("/attributes")
    @protected
    async def getAttributes(request):
        try:
            session = request.ctx.session
            params = request.args
            # Input validation
            [valid, error] = paginateValidator(params)
            if not valid:
                return resJson(resType.INVALID_PARAMS, error, len(error))

            async with session.begin():
                size = int(params.get('pageSize', 10))
                page = int(params.get('page', 1))
                sort = str(params.get('sortParam', 'created_at'))
                order = str(params.get('sortBy', 'DESC'))
                select_items: any = [
                    Attribute.id,
                    Attribute.odoo_id,
                    Attribute.name,
                    Attribute.display_name,
                    Attribute.value_ids,
                    Attribute.attribute_line_ids,
                    Attribute.is_used_on_products,
                    Attribute.product_tmpl_ids,
                    Attribute.created_at
                ]

                [stmt, count_] = paginatedQuery(
                    Attribute, sort, order, select_items, size, page)
                result = await session.execute(stmt)
                attributes = result.all()

                result_dict = [dict(attribute) for attribute in attributes]
                total_ = await session.execute(count_)
                total = total_.scalar()

            return resJson(resType.OK, result_dict, total)
        except:
            exceptionRaise('getAttributes')

    @p.get("/attribute/<pk_:uuid>")
    @protected
    async def getAttribute(request, pk_):
        try:
            session = request.ctx.session
            async with session.begin():
                attribute = await findRecordById(session, Attribute, pk_)

            if not attribute:
                return resJson(resType.NO_RECORD)

            return resJson(resType.OK, attribute.to_dict())
        except:
            exceptionRaise('getAttribute')

    # MARK: Support scalar and multi input

    @p.post("/attribute")
    @protected
    async def createAttribute(request):
        try:
            session = request.ctx.session
            body = request.json

            async with session.begin():
                if validate_list(body):
                    body_records = body
                else:
                    body_records = [body]

                # Input validation
                [valid, error] = postAttributeValidator(body_records)
                if not valid:
                    return resJson(resType.INVALID_PARAMS, error, len(error))

                output_list = []

                [new_list, update_list, redundant_ids] = await insertOrUpdate(session, body_records)
                if (not update_list) and (not redundant_ids):
                    # Post new record
                    result = await insertQuery(session, Attribute, new_list)
                else:
                    return resJson(resType.DUPLICATE, redundant_ids, len(redundant_ids))

                for u in result:
                    output_list.append(dict(u))

            return resJson(resType.OK, output_list, len(output_list))
        except:
            exceptionRaise('createAttribute')

    @p.delete("/attribute/<pk_:uuid>")
    @protected
    async def destroyAttribute(request, pk_):
        try:
            session = request.ctx.session
            resMsg = resType.SUCCESS_DEL
            async with session.begin():
                attribute = await findRecordById(session, Attribute, pk_)
                if not attribute:
                    return resJson(resType.NO_RECORD)

                destroy = await softDelbyId(session, Attribute, pk_)
                if not destroy:
                    resMsg = resType.FAIL_DELETE

            return resJson(resMsg, destroy)
        except:
            exceptionRaise('destroyAttribute')

    @p.put("/attribute/<pk_:uuid>")
    @protected
    async def updateAttribute(request, pk_):
        try:
            session = request.ctx.session
            b = request.json
            # Input validation
            [valid, error] = updateAttributeValidator(b)
            if not valid:
                return resJson(resType.INVALID_PARAMS, error, len(error))

            resMsg = resType.SUCCESS_UPD
            async with session.begin():
                attribute = await findRecordById(session, Attribute, pk_)
                if not attribute:
                    return resJson(resType.NO_RECORD)

                id = b.get('id', None)
                name = b.get('name', None)
                display_name = b.get('display_name', None)
                value_ids = b.get('value_ids', None)
                attribute_line_ids = b.get('attribute_line_ids', None)
                is_used_on_products = b.get('is_used_on_products', None)
                product_tmpl_ids = b.get('product_tmpl_ids', None)
                create_date = b.get('create_date', None)

                w_record = {}
                date_ = arrow.get(str(create_date)).datetime

                if id != attribute.odoo_id:
                    w_record['odoo_id'] = int(id)
                if name != attribute.name:
                    w_record['name'] = name
                if display_name != attribute.display_name:
                    w_record['display_name'] = display_name
                if list(value_ids) != attribute.value_ids:
                    w_record['value_ids'] = list(value_ids)
                if list(attribute_line_ids) != attribute.attribute_line_ids:
                    w_record['attribute_line_ids'] = list(attribute_line_ids)
                if bool(is_used_on_products) != attribute.is_used_on_products:
                    w_record['is_used_on_products'] = bool(is_used_on_products)
                if list(product_tmpl_ids) != attribute.product_tmpl_ids:
                    w_record['product_tmpl_ids'] = list(product_tmpl_ids)
                if date_.replace(tzinfo=None) != attribute.created_at:
                    w_record['created_at'] = date_.replace(tzinfo=None)

                if len(w_record) < 1:
                    return resJson(resType.NO_UPD, {})

                setAttr = await updateById(session, Attribute, pk_, w_record)
                if not setAttr:
                    resMsg = resType.FAIL_UPD

            return resJson(resMsg, setAttr)
        except:
            exceptionRaise('updateAttribute')

    @p.patch("/attribute")
    @protected
    async def addOrUpdateAttribute(request):
        try:
            session = request.ctx.session
            body = request.json

            async with session.begin():
                if validate_list(body):
                    body_records = body
                else:
                    body_records = [body]

                # Input validation
                [valid, error] = postAttributeValidator(body_records)
                if not valid:
                    return resJson(resType.INVALID_PARAMS, error, len(error))

                output_list = []

                [new_list, update_list, redundant_ids] = await insertOrUpdate(session, body_records)
                if new_list:
                    # Post new record
                    result = await insertQuery(session, Attribute, new_list)

                    for u in result:
                        output_list.append(u.id)

                if update_list:
                    result = await bulkUpdateQuery(session, Attribute, redundant_ids, update_list)

                    for u in result:
                        output_list.append(u)

                if not output_list:
                    return resJson(resType.NO_UPD, {})

            return resJson(resType.OK, output_list, len(output_list))
        except:
            exceptionRaise('addOrUpdateAttribute')


# -----------------
# functions section
# -----------------
async def insertOrUpdate(session, body, bg=False):
    try:
        new_list, update_list, redundant_ids = [], [], []
        # Sort body data by id
        body.sort(reverse=False, key=lambda e: e['id'])

        for b in body:
            id = b.get('id', None)
            name = b.get('name', None)
            display_name = b.get('display_name', None)
            value_ids = b.get('value_ids', None)
            attribute_line_ids = b.get('attribute_line_ids', None)
            is_used_on_products = b.get('is_used_on_products', None)
            product_tmpl_ids = b.get('product_tmpl_ids', None)
            create_date = b.get('create_date', None)
            w_record = {}

            if not bg:
                attribute = await findRecordByColumn(session, Attribute, Attribute.odoo_id, int(id), False)
            else:
                attribute = await findRecordByColumnCron(session, Attribute, Attribute.odoo_id, int(id), False)
            if not attribute:
                # register record
                date_ = arrow.get(str(create_date)).datetime
                w_record = {
                    "odoo_id": int(id),
                    "name": str(name),
                    "display_name": str(display_name),
                    "value_ids": list(value_ids),
                    "attribute_line_ids": list(attribute_line_ids),
                    "is_used_on_products": bool(is_used_on_products),
                    "product_tmpl_ids": list(product_tmpl_ids),
                    "created_at": date_.replace(tzinfo=None)
                }
                new_list.append(w_record)
            else:
                # update record
                date_ = arrow.get(str(create_date)).datetime

                if name != attribute.name:
                    w_record['name'] = name
                if display_name != attribute.display_name:
                    w_record['display_name'] = display_name
                if list(value_ids) != attribute.value_ids:
                    w_record['value_ids'] = list(value_ids)
                if list(attribute_line_ids) != attribute.attribute_line_ids:
                    w_record['attribute_line_ids'] = list(attribute_line_ids)
                if bool(is_used_on_products) != attribute.is_used_on_products:
                    w_record['is_used_on_products'] = bool(is_used_on_products)
                if list(product_tmpl_ids) != attribute.product_tmpl_ids:
                    w_record['product_tmpl_ids'] = list(product_tmpl_ids)
                if date_.replace(tzinfo=None) != attribute.created_at:
                    w_record['created_at'] = date_.replace(tzinfo=None)

                if w_record:
                    w_record['odoo_id'] = attribute.odoo_id
                    update_list.append(w_record)

                redundant_ids.append(int(id))

        return [new_list, update_list, redundant_ids]
    except:
        exceptionRaise('insertOrUpdate')


# Bulk update
async def bulkUpdateQuery(session_, model_, pk_, values_):
    try:
        mappings = []
        for x in values_:
            print(x)
            stmt = update(model_).where(model_.odoo_id == x['odoo_id']).\
                where(model_.deleted_at.is_(None)).\
                values(x).\
                returning(model_.id)

            result = await session_.execute(stmt)
            mappings.append(result.scalar())

        return mappings
    except:
        exceptionRaise('bulkUpdateQuery')


async def cronAddUpdateProcess(session, body):
    if validate_list(body):
        body_records = body
    else:
        body_records = [body]
    output_list = []
    [new_list, update_list, redundant_ids] = await insertOrUpdate(session, body_records, True)
    if new_list:
        # Post new record
        result = await insertQuery(session, Attribute, new_list)

        for u in result:
            output_list.append(u.id)

    if update_list:
        result = await bulkUpdateQuery(session, Attribute, redundant_ids, update_list)

        for u in result:
            output_list.append(u)

    if (not output_list) and (not redundant_ids):
        await session.rollback()

    return output_list


# Cron auto feed to db func
async def migrateAttributeToDB(app):
    async with app.db.begin() as conn:
        # TODO: async func can await call from odoo, need improvements?
        output = await get_attr()
        output_list = await cronAddUpdateProcess(conn, output)

        await conn.commit()
        await conn.close()
    return True
