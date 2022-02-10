from helpers.func import (
    resJson,
    resType,
    exceptionRaise,
    validate_list
)
from helpers.validator import paginateValidator, postProdAttributeLineValidator, updateProdAttributeLineValidator
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
from models.product_attribute_line import ProductAttributeLine
from utils.auth import protected
from sqlalchemy import update
from odoo.main import get_prod_attr_line

import arrow

# -----------------
# API Class Section
# -----------------


class ProductAttributeLineController():
    p = Blueprint('prod_attribute_lines', url_prefix='/')

    @p.get("/prod-attribute-lines")
    @protected
    async def getProdAttributeLines(request):
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
                    ProductAttributeLine.id,
                    ProductAttributeLine.odoo_id,
                    ProductAttributeLine.display_name,
                    ProductAttributeLine.active,
                    ProductAttributeLine.product_tmpl_id,
                    ProductAttributeLine.attribute_id,
                    ProductAttributeLine.value_ids,
                    ProductAttributeLine.product_template_value_ids,
                    ProductAttributeLine.created_at
                ]

                [stmt, count_] = paginatedQuery(
                    ProductAttributeLine, sort, order, select_items, size, page)
                result = await session.execute(stmt)
                attribute_lines = result.all()

                result_dict = [dict(attribute_line)
                               for attribute_line in attribute_lines]
                total_ = await session.execute(count_)
                total = total_.scalar()

            return resJson(resType.OK, result_dict, total)
        except:
            exceptionRaise('getProdAttributeLines')

    @p.get("/prod-attribute-line/<pk_:uuid>")
    @protected
    async def getProdAttributeLine(request, pk_):
        try:
            session = request.ctx.session
            async with session.begin():
                attribute_line = await findRecordById(session, ProductAttributeLine, pk_)

            if not attribute_line:
                return resJson(resType.NO_RECORD)

            return resJson(resType.OK, attribute_line.to_dict())
        except:
            exceptionRaise('getProdAttributeLine')


    # MARK: Support scalar and multi input
    @p.post("/prod-attribute-line")
    @protected
    async def createProdAttributeLine(request):
        try:
            session = request.ctx.session
            body = request.json

            async with session.begin():
                if validate_list(body):
                    body_records = body
                else:
                    body_records = [body]

                # Input validation
                [valid, error] = postProdAttributeLineValidator(body_records)
                if not valid:
                    return resJson(resType.INVALID_PARAMS, error, len(error))

                output_list = []

                [new_list, update_list, redundant_ids] = await insertOrUpdate(session, body_records)
                if (not update_list) and (not redundant_ids):
                    # Post new record
                    result = await insertQuery(session, ProductAttributeLine, new_list)
                else:
                    return resJson(resType.DUPLICATE, redundant_ids, len(redundant_ids))

                for u in result:
                    output_list.append(dict(u))

            return resJson(resType.OK, output_list, len(output_list))
        except:
            exceptionRaise('createProdAttributeLine')

    @p.delete("/prod-attribute-line/<pk_:uuid>")
    @protected
    async def destroyProdAttributeLine(request, pk_):
        try:
            session = request.ctx.session
            resMsg = resType.SUCCESS_DEL
            async with session.begin():
                attribute_line = await findRecordById(session, ProductAttributeLine, pk_)
                if not attribute_line:
                    return resJson(resType.NO_RECORD)

                destroy = await softDelbyId(session, ProductAttributeLine, pk_)
                if not destroy:
                    resMsg = resType.FAIL_DELETE

            return resJson(resMsg, destroy)
        except:
            exceptionRaise('destroyProdAttributeLine')

    @p.put("/prod-attribute-line/<pk_:uuid>")
    @protected
    async def updateProdAttributeLine(request, pk_):
        try:
            session = request.ctx.session
            b = request.json
            # Input validation
            [valid, error] = updateProdAttributeLineValidator(b)
            if not valid:
                return resJson(resType.INVALID_PARAMS, error, len(error))

            resMsg = resType.SUCCESS_UPD
            async with session.begin():
                attribute_line = await findRecordById(session, ProductAttributeLine, pk_)
                if not attribute_line:
                    return resJson(resType.NO_RECORD)

                id = b.get('id', None)
                display_name = b.get('display_name', None)
                active = b.get('active', None)
                product_tmpl_id = b.get('product_tmpl_id', None)
                attribute_id = b.get('attribute_id', None)
                value_ids = b.get('value_ids', None)
                product_template_value_ids = b.get('product_template_value_ids', None)
                create_date = b.get('create_date', None)

                w_record = {}
                date_ = arrow.get(str(create_date)).datetime

                if id != attribute_line.odoo_id:
                    w_record['odoo_id'] = int(id)
                if display_name != attribute_line.display_name:
                    w_record['display_name'] = display_name
                if bool(active) != attribute_line.active:
                    w_record['active'] = bool(active)
                if int(product_tmpl_id[0]) != attribute_line.product_tmpl_id:
                    w_record['product_tmpl_id'] = int(
                        product_tmpl_id[0])
                if int(attribute_id[0]) != attribute_line.attribute_id:
                    w_record['attribute_id'] = int(attribute_id[0])
                if list(value_ids) != attribute_line.value_ids:
                    w_record['value_ids'] = list(
                        value_ids)
                if list(product_template_value_ids) != attribute_line.product_template_value_ids:
                    w_record['product_template_value_ids'] = list(
                        product_template_value_ids)
                if date_.replace(tzinfo=None) != attribute_line.created_at:
                    w_record['created_at'] = date_.replace(tzinfo=None)

                if len(w_record) < 1:
                    return resJson(resType.NO_UPD, {})

                setAttr = await updateById(session, ProductAttributeLine, pk_, w_record)
                if not setAttr:
                    resMsg = resType.FAIL_UPD

            return resJson(resMsg, setAttr)
        except:
            exceptionRaise('updateProdAttributeLine')

    @p.patch("/prod-attribute-line")
    @protected
    async def addOrUpdateProdAttributeLine(request):
        try:
            session = request.ctx.session
            body = request.json

            async with session.begin():
                if validate_list(body):
                    body_records = body
                else:
                    body_records = [body]

                # Input validation
                [valid, error] = postProdAttributeLineValidator(body_records)
                if not valid:
                    return resJson(resType.INVALID_PARAMS, error, len(error))

                output_list = []

                [new_list, update_list, redundant_ids] = await insertOrUpdate(session, body_records)
                if new_list:
                    # Post new record
                    result = await insertQuery(session, ProductAttributeLine, new_list)

                    for u in result:
                        output_list.append(u.id)

                if update_list:
                    result = await bulkUpdateQuery(session, ProductAttributeLine, redundant_ids, update_list)

                    for u in result:
                        output_list.append(u)

                if not output_list:
                    return resJson(resType.NO_UPD, {})

            return resJson(resType.OK, output_list, len(output_list))
        except:
            exceptionRaise('addOrUpdateProdAttributeLine')


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
            display_name = b.get('display_name', None)
            active = b.get('active', None)
            product_tmpl_id = b.get('product_tmpl_id', None)
            attribute_id = b.get('attribute_id', None)
            value_ids = b.get('value_ids', None)
            product_template_value_ids = b.get('product_template_value_ids', None)
            create_date = b.get('create_date', None)
            w_record = {}

            if not bg:
                attribute_line = await findRecordByColumn(session, ProductAttributeLine, ProductAttributeLine.odoo_id, int(id), False)
            else:
                attribute_line = await findRecordByColumnCron(session, ProductAttributeLine, ProductAttributeLine.odoo_id, int(id), False)
            if not attribute_line:
                # register record
                date_ = arrow.get(str(create_date)).datetime
                w_record = {
                    "odoo_id": int(id),
                    "display_name": str(display_name),
                    "active": bool(active),
                    "product_tmpl_id": int(product_tmpl_id[0]),
                    "attribute_id": int(attribute_id[0]),
                    "value_ids": list(value_ids),
                    "product_template_value_ids": list(product_template_value_ids),
                    "created_at": date_.replace(tzinfo=None)
                }
                new_list.append(w_record)
            else:
                # update record
                date_ = arrow.get(str(create_date)).datetime

                if display_name != attribute_line.display_name:
                    w_record['display_name'] = display_name
                if bool(active) != attribute_line.active:
                    w_record['active'] = bool(active)
                if int(product_tmpl_id[0]) != attribute_line.product_tmpl_id:
                    w_record['product_tmpl_id'] = int(product_tmpl_id[0])
                if int(attribute_id[0]) != attribute_line.attribute_id:
                    w_record['attribute_id'] = int(attribute_id[0])
                if list(value_ids) != attribute_line.value_ids:
                    w_record['value_ids'] = list(
                        value_ids)
                if list(product_template_value_ids) != attribute_line.product_template_value_ids:
                    w_record['product_template_value_ids'] = list(
                        product_template_value_ids)
                if date_.replace(tzinfo=None) != attribute_line.created_at:
                    w_record['created_at'] = date_.replace(tzinfo=None)

                if w_record:
                    w_record['odoo_id'] = attribute_line.odoo_id
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
        result = await insertQuery(session, ProductAttributeLine, new_list)

        for u in result:
            output_list.append(u.id)

    if update_list:
        result = await bulkUpdateQuery(session, ProductAttributeLine, redundant_ids, update_list)

        for u in result:
            output_list.append(u)

    if (not output_list) and (not redundant_ids):
        await session.rollback()

    return output_list


# Cron auto feed to db func
async def migrateProdAttributeLineToDB(app):
    async with app.ctx.db.begin() as conn:
        # TODO: async func can await call from odoo, need improvements?
        output = await get_prod_attr_line()
        _ = await cronAddUpdateProcess(conn, output)

        await conn.commit()
        await conn.close()
    return True
