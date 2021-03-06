from helpers.func import (
    resJson,
    resType,
    exceptionRaise,
    validate_list
)
from helpers.validator import paginateValidator, postAttributeValueValidator, updateAttributeValueValidator
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
from models.attribute_value import AttributeValue
from utils.auth import protected
from sqlalchemy import update
from odoo.main import get_attr_value

import arrow

# -----------------
# API Class Section
# -----------------


class AttributeValueController():
    p = Blueprint('attribute_value', url_prefix='/')

    @p.get("/attribute-values")
    @protected
    async def getAttributeValues(request):
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
                    AttributeValue.id,
                    AttributeValue.odoo_id,
                    AttributeValue.name,
                    AttributeValue.display_name,
                    AttributeValue.attribute_id,
                    AttributeValue.pav_attribute_line_ids,
                    AttributeValue.is_used_on_products,
                    AttributeValue.created_at
                ]

                [stmt, count_] = paginatedQuery(
                    AttributeValue, sort, order, select_items, size, page)
                result = await session.execute(stmt)
                attribute_values = result.all()

                result_dict = [dict(attribute_value)
                               for attribute_value in attribute_values]
                total_ = await session.execute(count_)
                total = total_.scalar()

            return resJson(resType.OK, result_dict, total)
        except:
            exceptionRaise('getAttributeValues')

    @p.get("/attribute-value/<pk_:uuid>")
    @protected
    async def getAttributeValue(request, pk_):
        try:
            session = request.ctx.session
            async with session.begin():
                attribute_value = await findRecordById(session, AttributeValue, pk_)

            if not attribute_value:
                return resJson(resType.NO_RECORD)

            return resJson(resType.OK, attribute_value.to_dict())
        except:
            exceptionRaise('getAttributeValue')

    # MARK: Support scalar and multi input

    @p.post("/attribute-value")
    @protected
    async def createAttributeValue(request):
        try:
            session = request.ctx.session
            body = request.json

            async with session.begin():
                if validate_list(body):
                    body_records = body
                else:
                    body_records = [body]

                # Input validation
                [valid, error] = postAttributeValueValidator(body_records)
                if not valid:
                    return resJson(resType.INVALID_PARAMS, error, len(error))

                output_list = []

                [new_list, update_list, redundant_ids] = await insertOrUpdate(session, body_records)
                if (not update_list) and (not redundant_ids):
                    # Post new record
                    result = await insertQuery(session, AttributeValue, new_list)
                else:
                    return resJson(resType.DUPLICATE, redundant_ids, len(redundant_ids))

                for u in result:
                    output_list.append(dict(u))

            return resJson(resType.OK, output_list, len(output_list))
        except:
            exceptionRaise('createAttributeValue')

    @p.delete("/attribute-value/<pk_:uuid>")
    @protected
    async def destroyAttributeValue(request, pk_):
        try:
            session = request.ctx.session
            resMsg = resType.SUCCESS_DEL
            async with session.begin():
                attribute_value = await findRecordById(session, AttributeValue, pk_)
                if not attribute_value:
                    return resJson(resType.NO_RECORD)

                destroy = await softDelbyId(session, AttributeValue, pk_)
                if not destroy:
                    resMsg = resType.FAIL_DELETE

            return resJson(resMsg, destroy)
        except:
            exceptionRaise('destroyAttributeValue')

    @p.put("/attribute-value/<pk_:uuid>")
    @protected
    async def updateAttributeValue(request, pk_):
        try:
            session = request.ctx.session
            b = request.json
            # Input validation
            [valid, error] = updateAttributeValueValidator(b)
            if not valid:
                return resJson(resType.INVALID_PARAMS, error, len(error))

            resMsg = resType.SUCCESS_UPD
            async with session.begin():
                attribute_value = await findRecordById(session, AttributeValue, pk_)
                if not attribute_value:
                    return resJson(resType.NO_RECORD)

                id = b.get('id', None)
                name = b.get('name', None)
                display_name = b.get('display_name', None)
                attribute_id = b.get('attribute_id', None)
                pav_attribute_line_ids = b.get('pav_attribute_line_ids', None)
                is_used_on_products = b.get('is_used_on_products', None)
                create_date = b.get('create_date', None)

                w_record = {}
                date_ = arrow.get(str(create_date)).datetime

                if id != attribute_value.odoo_id:
                    w_record['odoo_id'] = int(id)
                if name != attribute_value.name:
                    w_record['name'] = name
                if display_name != attribute_value.display_name:
                    w_record['display_name'] = display_name
                if int(attribute_id[0]) != attribute_value.attribute_id:
                    w_record['attribute_id'] = int(attribute_id[0])
                if list(pav_attribute_line_ids) != attribute_value.pav_attribute_line_ids:
                    w_record['pav_attribute_line_ids'] = list(
                        pav_attribute_line_ids)
                if bool(is_used_on_products) != attribute_value.is_used_on_products:
                    w_record['is_used_on_products'] = bool(is_used_on_products)
                if date_.replace(tzinfo=None) != attribute_value.created_at:
                    w_record['created_at'] = date_.replace(tzinfo=None)

                if len(w_record) < 1:
                    return resJson(resType.NO_UPD, {})

                setAttr = await updateById(session, AttributeValue, pk_, w_record)
                if not setAttr:
                    resMsg = resType.FAIL_UPD

            return resJson(resMsg, setAttr)
        except:
            exceptionRaise('updateAttributeValue')

    @p.patch("/attribute-value")
    @protected
    async def addOrUpdateAttributeValue(request):
        try:
            session = request.ctx.session
            body = request.json

            async with session.begin():
                if validate_list(body):
                    body_records = body
                else:
                    body_records = [body]

                # Input validation
                [valid, error] = postAttributeValueValidator(body_records)
                if not valid:
                    return resJson(resType.INVALID_PARAMS, error, len(error))

                output_list = []

                [new_list, update_list, redundant_ids] = await insertOrUpdate(session, body_records)
                if new_list:
                    # Post new record
                    result = await insertQuery(session, AttributeValue, new_list)

                    for u in result:
                        output_list.append(u.id)

                if update_list:
                    result = await bulkUpdateQuery(session, AttributeValue, redundant_ids, update_list)

                    for u in result:
                        output_list.append(u)

                if not output_list:
                    return resJson(resType.NO_UPD, {})

            return resJson(resType.OK, output_list, len(output_list))
        except:
            exceptionRaise('addOrUpdateAttributeValue')


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
            attribute_id = b.get('attribute_id', None)
            pav_attribute_line_ids = b.get('pav_attribute_line_ids', None)
            is_used_on_products = b.get('is_used_on_products', None)
            create_date = b.get('create_date', None)
            w_record = {}

            if not bg:
                attribute_value = await findRecordByColumn(session, AttributeValue, AttributeValue.odoo_id, int(id), False)
            else:
                attribute_value = await findRecordByColumnCron(session, AttributeValue, AttributeValue.odoo_id, int(id), False)
            if not attribute_value:
                # register record
                date_ = arrow.get(str(create_date)).datetime
                w_record = {
                    "odoo_id": int(id),
                    "name": str(name),
                    "display_name": str(display_name),
                    "attribute_id": int(attribute_id[0]),
                    "pav_attribute_line_ids": list(pav_attribute_line_ids),
                    "is_used_on_products": bool(is_used_on_products),
                    "created_at": date_.replace(tzinfo=None)
                }
                new_list.append(w_record)
            else:
                # update record
                date_ = arrow.get(str(create_date)).datetime

                if name != attribute_value.name:
                    w_record['name'] = name
                if display_name != attribute_value.display_name:
                    w_record['display_name'] = display_name
                if int(attribute_id[0]) != attribute_value.attribute_id:
                    w_record['attribute_id'] = int(attribute_id[0])
                if list(pav_attribute_line_ids) != attribute_value.pav_attribute_line_ids:
                    w_record['pav_attribute_line_ids'] = list(
                        pav_attribute_line_ids)
                if bool(is_used_on_products) != attribute_value.is_used_on_products:
                    w_record['is_used_on_products'] = bool(is_used_on_products)
                if date_.replace(tzinfo=None) != attribute_value.created_at:
                    w_record['created_at'] = date_.replace(tzinfo=None)

                if w_record:
                    w_record['odoo_id'] = attribute_value.odoo_id
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
        result = await insertQuery(session, AttributeValue, new_list)

        for u in result:
            output_list.append(u.id)

    if update_list:
        result = await bulkUpdateQuery(session, AttributeValue, redundant_ids, update_list)

        for u in result:
            output_list.append(u)

    if (not output_list) and (not redundant_ids):
        await session.rollback()

    return output_list


# Cron auto feed to db func
async def migrateAttributeValueToDB(app):
    async with app.ctx.db.begin() as conn:
        # TODO: async func can await call from odoo, need improvements?
        output = await get_attr_value()
        _ = await cronAddUpdateProcess(conn, output)

        await conn.commit()
        await conn.close()
    return True
