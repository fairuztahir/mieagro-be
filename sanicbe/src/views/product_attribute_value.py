from helpers.func import (
    resJson,
    resType,
    exceptionRaise,
    validate_list
)
from helpers.validator import paginateValidator, postProdAttributeValueValidator, updateProdAttributeValueValidator
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
from models.product_attribute_value import ProductAttributeValue
from utils.auth import protected
from sqlalchemy import update
from odoo.main import get_prod_attr_value

import arrow

# -----------------
# API Class Section
# -----------------


class ProductAttributeValueController():
    p = Blueprint('prod_attribute_value', url_prefix='/')

    @p.get("/prod-attribute-values")
    @protected
    async def getProdAttributeValues(request):
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
                    ProductAttributeValue.id,
                    ProductAttributeValue.odoo_id,
                    ProductAttributeValue.name,
                    ProductAttributeValue.display_name,
                    ProductAttributeValue.ptav_active,
                    ProductAttributeValue.product_attribute_value_id,
                    ProductAttributeValue.attribute_line_id,
                    ProductAttributeValue.price_extra,
                    ProductAttributeValue.exclude_for,
                    ProductAttributeValue.product_tmpl_id,
                    ProductAttributeValue.attribute_id,
                    ProductAttributeValue.ptav_product_variant_ids,
                    ProductAttributeValue.is_custom,
                    ProductAttributeValue.display_type,
                    ProductAttributeValue.created_at
                ]

                [stmt, count_] = paginatedQuery(
                    ProductAttributeValue, sort, order, select_items, size, page)
                result = await session.execute(stmt)
                attribute_values = result.all()

                result_dict = [dict(attribute_value)
                               for attribute_value in attribute_values]
                total_ = await session.execute(count_)
                total = total_.scalar()

            return resJson(resType.OK, result_dict, total)
        except:
            exceptionRaise('getProdAttributeValues')

    @p.get("/prod-attribute-value/<pk_:uuid>")
    @protected
    async def getProdAttributeValue(request, pk_):
        try:
            session = request.ctx.session
            async with session.begin():
                attribute_value = await findRecordById(session, ProductAttributeValue, pk_)

            if not attribute_value:
                return resJson(resType.NO_RECORD)

            return resJson(resType.OK, attribute_value.to_dict())
        except:
            exceptionRaise('getProdAttributeValue')


    # MARK: Support scalar and multi input
    @p.post("/prod-attribute-value")
    @protected
    async def createProdAttributeValue(request):
        try:
            session = request.ctx.session
            body = request.json

            async with session.begin():
                if validate_list(body):
                    body_records = body
                else:
                    body_records = [body]

                # Input validation
                [valid, error] = postProdAttributeValueValidator(body_records)
                if not valid:
                    return resJson(resType.INVALID_PARAMS, error, len(error))

                output_list = []

                [new_list, update_list, redundant_ids] = await insertOrUpdate(session, body_records)
                if (not update_list) and (not redundant_ids):
                    # Post new record
                    result = await insertQuery(session, ProductAttributeValue, new_list)
                else:
                    return resJson(resType.DUPLICATE, redundant_ids, len(redundant_ids))

                for u in result:
                    output_list.append(dict(u))

            return resJson(resType.OK, output_list, len(output_list))
        except:
            exceptionRaise('createProdAttributeValue')

    @p.delete("/prod-attribute-value/<pk_:uuid>")
    @protected
    async def destroyProdAttributeValue(request, pk_):
        try:
            session = request.ctx.session
            resMsg = resType.SUCCESS_DEL
            async with session.begin():
                attribute_value = await findRecordById(session, ProductAttributeValue, pk_)
                if not attribute_value:
                    return resJson(resType.NO_RECORD)

                destroy = await softDelbyId(session, ProductAttributeValue, pk_)
                if not destroy:
                    resMsg = resType.FAIL_DELETE

            return resJson(resMsg, destroy)
        except:
            exceptionRaise('destroyProdAttributeValue')

    @p.put("/prod-attribute-value/<pk_:uuid>")
    @protected
    async def updateProdAttributeValue(request, pk_):
        try:
            session = request.ctx.session
            b = request.json
            # Input validation
            [valid, error] = updateProdAttributeValueValidator(b)
            if not valid:
                return resJson(resType.INVALID_PARAMS, error, len(error))

            resMsg = resType.SUCCESS_UPD
            async with session.begin():
                attribute_value = await findRecordById(session, ProductAttributeValue, pk_)
                if not attribute_value:
                    return resJson(resType.NO_RECORD)

                id = b.get('id', None)
                name = b.get('name', None)
                display_name = b.get('display_name', None)
                ptav_active = b.get('ptav_active', None)
                product_attribute_value_id = b.get('product_attribute_value_id', None)
                attribute_line_id = b.get('attribute_line_id', None)
                price_extra = b.get('price_extra', None)
                exclude_for = b.get('exclude_for', None)
                product_tmpl_id = b.get('product_tmpl_id', None)
                attribute_id = b.get('attribute_id', None)
                ptav_product_variant_ids = b.get('ptav_product_variant_ids', None)
                is_custom = b.get('is_custom', None)
                display_type = b.get('display_type', None)
                create_date = b.get('create_date', None)

                w_record = {}
                date_ = arrow.get(str(create_date)).datetime

                if id != attribute_value.odoo_id:
                    w_record['odoo_id'] = int(id)
                if name != attribute_value.name:
                    w_record['name'] = name
                if display_name != attribute_value.display_name:
                    w_record['display_name'] = display_name
                if bool(ptav_active) != attribute_value.ptav_active:
                    w_record['ptav_active'] = bool(ptav_active)
                if int(product_attribute_value_id[0]) != attribute_value.product_attribute_value_id:
                    w_record['product_attribute_value_id'] = int(
                        product_attribute_value_id[0])
                if int(attribute_line_id[0]) != attribute_value.attribute_line_id:
                    w_record['attribute_line_id'] = int(attribute_line_id[0])
                if float(price_extra) != attribute_value.price_extra:
                    w_record['price_extra'] = float(price_extra)
                if list(exclude_for) != attribute_value.exclude_for:
                    w_record['exclude_for'] = list(
                        exclude_for)
                if int(product_tmpl_id[0]) != attribute_value.product_tmpl_id:
                    w_record['product_tmpl_id'] = int(product_tmpl_id[0])
                if int(attribute_id[0]) != attribute_value.attribute_id:
                    w_record['attribute_id'] = int(attribute_id[0])
                if list(ptav_product_variant_ids) != attribute_value.ptav_product_variant_ids:
                    w_record['ptav_product_variant_ids'] = list(
                        ptav_product_variant_ids)
                if bool(is_custom) != attribute_value.is_custom:
                    w_record['is_custom'] = bool(is_custom)
                if display_type != attribute_value.display_type:
                    w_record['display_type'] = display_type
                if date_.replace(tzinfo=None) != attribute_value.created_at:
                    w_record['created_at'] = date_.replace(tzinfo=None)

                if len(w_record) < 1:
                    return resJson(resType.NO_UPD, {})

                setAttr = await updateById(session, ProductAttributeValue, pk_, w_record)
                if not setAttr:
                    resMsg = resType.FAIL_UPD

            return resJson(resMsg, setAttr)
        except:
            exceptionRaise('updateProdAttributeValue')

    @p.patch("/prod-attribute-value")
    @protected
    async def addOrUpdateProdAttributeValue(request):
        try:
            session = request.ctx.session
            body = request.json

            async with session.begin():
                if validate_list(body):
                    body_records = body
                else:
                    body_records = [body]

                # Input validation
                [valid, error] = postProdAttributeValueValidator(body_records)
                if not valid:
                    return resJson(resType.INVALID_PARAMS, error, len(error))

                output_list = []

                [new_list, update_list, redundant_ids] = await insertOrUpdate(session, body_records)
                if new_list:
                    # Post new record
                    result = await insertQuery(session, ProductAttributeValue, new_list)

                    for u in result:
                        output_list.append(u.id)

                if update_list:
                    result = await bulkUpdateQuery(session, ProductAttributeValue, redundant_ids, update_list)

                    for u in result:
                        output_list.append(u)

                if not output_list:
                    return resJson(resType.NO_UPD, {})

            return resJson(resType.OK, output_list, len(output_list))
        except:
            exceptionRaise('addOrUpdateProdAttributeValue')


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
            ptav_active = b.get('ptav_active', None)
            product_attribute_value_id = b.get('product_attribute_value_id', None)
            attribute_line_id = b.get('attribute_line_id', None)
            price_extra = b.get('price_extra', None)
            exclude_for = b.get('exclude_for', None)
            product_tmpl_id = b.get('product_tmpl_id', None)
            attribute_id = b.get('attribute_id', None)
            ptav_product_variant_ids = b.get('ptav_product_variant_ids', None)
            is_custom = b.get('is_custom', None)
            display_type = b.get('display_type', None)
            create_date = b.get('create_date', None)
            w_record = {}

            if not bg:
                attribute_value = await findRecordByColumn(session, ProductAttributeValue, ProductAttributeValue.odoo_id, int(id), False)
            else:
                attribute_value = await findRecordByColumnCron(session, ProductAttributeValue, ProductAttributeValue.odoo_id, int(id), False)
            if not attribute_value:
                # register record
                date_ = arrow.get(str(create_date)).datetime
                w_record = {
                    "odoo_id": int(id),
                    "name": str(name),
                    "display_name": str(display_name),
                    "ptav_active": bool(ptav_active),
                    "product_attribute_value_id": int(product_attribute_value_id[0]),
                    "attribute_line_id": int(attribute_line_id[0]),
                    "price_extra": float(price_extra),
                    "exclude_for": list(exclude_for),
                    "product_tmpl_id": int(product_tmpl_id[0]),
                    "attribute_id": int(attribute_id[0]),
                    "ptav_product_variant_ids": list(ptav_product_variant_ids),
                    "is_custom": bool(is_custom),
                    "display_type": str(display_type),
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
                if bool(ptav_active) != attribute_value.ptav_active:
                    w_record['ptav_active'] = bool(ptav_active)
                if int(product_attribute_value_id[0]) != attribute_value.product_attribute_value_id:
                    w_record['product_attribute_value_id'] = int(
                        product_attribute_value_id[0])
                if int(attribute_line_id[0]) != attribute_value.attribute_line_id:
                    w_record['attribute_line_id'] = int(attribute_line_id[0])
                if float(price_extra) != attribute_value.price_extra:
                    w_record['price_extra'] = float(price_extra)
                if list(exclude_for) != attribute_value.exclude_for:
                    w_record['exclude_for'] = list(
                        exclude_for)
                if int(product_tmpl_id[0]) != attribute_value.product_tmpl_id:
                    w_record['product_tmpl_id'] = int(product_tmpl_id[0])
                if int(attribute_id[0]) != attribute_value.attribute_id:
                    w_record['attribute_id'] = int(attribute_id[0])
                if list(ptav_product_variant_ids) != attribute_value.ptav_product_variant_ids:
                    w_record['ptav_product_variant_ids'] = list(
                        ptav_product_variant_ids)
                if bool(is_custom) != attribute_value.is_custom:
                    w_record['is_custom'] = bool(is_custom)
                if display_type != attribute_value.display_type:
                    w_record['display_type'] = display_type
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
        result = await insertQuery(session, ProductAttributeValue, new_list)

        for u in result:
            output_list.append(u.id)

    if update_list:
        result = await bulkUpdateQuery(session, ProductAttributeValue, redundant_ids, update_list)

        for u in result:
            output_list.append(u)

    if (not output_list) and (not redundant_ids):
        await session.rollback()

    return output_list


# Cron auto feed to db func
async def migrateProdAttributeValueToDB(app):
    async with app.ctx.db.begin() as conn:
        # TODO: async func can await call from odoo, need improvements?
        output = await get_prod_attr_value()
        _ = await cronAddUpdateProcess(conn, output)

        await conn.commit()
        await conn.close()
    return True
