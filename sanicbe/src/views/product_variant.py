from helpers.func import (
    resJson,
    resType,
    exceptionRaise,
    validate_list
)
from helpers.validator import paginateValidator, postProdVariantValidator, updateProdVariantValidator
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
from models.product_variant import ProductVariant
from utils.auth import protected
from sqlalchemy import update
from odoo.main import get_prod_detail_by_id

import arrow

# -----------------
# API Class Section
# -----------------


class ProductVariantController():
    p = Blueprint('prod_variants', url_prefix='/')

    @p.get("/prod-variants")
    @protected
    async def getProdVariants(request):
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
                    ProductVariant.id,
                    ProductVariant.odoo_id,
                    ProductVariant.name,
                    ProductVariant.display_name,
                    ProductVariant.code,
                    ProductVariant.default_code,
                    ProductVariant.description,
                    ProductVariant.active,
                    ProductVariant.product_tmpl_id,
                    ProductVariant.barcode,
                    ProductVariant.is_product_variant,
                    ProductVariant.available_in_pos,
                    ProductVariant.attribute_line_ids,
                    ProductVariant.price,
                    ProductVariant.price_extra,
                    ProductVariant.free_qty,
                    ProductVariant.qty_available,
                    ProductVariant.incoming_qty,
                    ProductVariant.outgoing_qty,
                    ProductVariant.created_at
                ]

                [stmt, count_] = paginatedQuery(
                    ProductVariant, sort, order, select_items, size, page)
                result = await session.execute(stmt)
                variants = result.all()

                result_dict = [dict(variant)
                               for variant in variants]
                total_ = await session.execute(count_)
                total = total_.scalar()

            return resJson(resType.OK, result_dict, total)
        except:
            exceptionRaise('getProdVariants')

    @p.get("/prod-variant/<pk_:uuid>")
    @protected
    async def getProdVariant(request, pk_):
        try:
            session = request.ctx.session
            async with session.begin():
                variant = await findRecordById(session, ProductVariant, pk_)

            if not variant:
                return resJson(resType.NO_RECORD)

            return resJson(resType.OK, variant.to_dict())
        except:
            exceptionRaise('getProdVariant')

    # MARK: Support scalar and multi input

    @p.post("/prod-variant")
    @protected
    async def createProdVariant(request):
        try:
            session = request.ctx.session
            body = request.json

            async with session.begin():
                if validate_list(body):
                    body_records = body
                else:
                    body_records = [body]

                # Input validation
                [valid, error] = postProdVariantValidator(body_records)
                if not valid:
                    return resJson(resType.INVALID_PARAMS, error, len(error))

                output_list = []

                [new_list, update_list, redundant_ids] = await insertOrUpdate(session, body_records)
                if (not update_list) and (not redundant_ids):
                    # Post new record
                    result = await insertQuery(session, ProductVariant, new_list)
                else:
                    return resJson(resType.DUPLICATE, redundant_ids, len(redundant_ids))

                for u in result:
                    output_list.append(dict(u))

            return resJson(resType.OK, output_list, len(output_list))
        except:
            exceptionRaise('createProdVariant')

    @p.delete("/prod-variant/<pk_:uuid>")
    @protected
    async def destroyProdVariant(request, pk_):
        try:
            session = request.ctx.session
            resMsg = resType.SUCCESS_DEL
            async with session.begin():
                variant = await findRecordById(session, ProductVariant, pk_)
                if not variant:
                    return resJson(resType.NO_RECORD)

                destroy = await softDelbyId(session, ProductVariant, pk_)
                if not destroy:
                    resMsg = resType.FAIL_DELETE

            return resJson(resMsg, destroy)
        except:
            exceptionRaise('destroyProdVariant')

    @p.put("/prod-variant/<pk_:uuid>")
    @protected
    async def updateProdVariant(request, pk_):
        try:
            session = request.ctx.session
            b = request.json
            # Input validation
            [valid, error] = updateProdVariantValidator(b)
            if not valid:
                return resJson(resType.INVALID_PARAMS, error, len(error))

            resMsg = resType.SUCCESS_UPD
            async with session.begin():
                variant = await findRecordById(session, ProductVariant, pk_)
                if not variant:
                    return resJson(resType.NO_RECORD)

                id = b.get('id', None)
                name = b.get('name', None)
                display_name = b.get('display_name', None)
                code = b.get('code', None)
                default_code = b.get('default_code', None)
                description = b.get('description', None)
                active = b.get('active', None)
                product_tmpl_id = b.get('product_tmpl_id', None)
                barcode = b.get('barcode', None)
                if barcode == False:
                    barcode = None
                else:
                    barcode = str(barcode)

                is_product_variant = b.get('is_product_variant', None)
                available_in_pos = b.get('available_in_pos', None)
                attribute_line_ids = b.get('attribute_line_ids', None)
                price = b.get('price', None)
                price_extra = b.get('price_extra', None)
                free_qty = b.get('free_qty', None)
                qty_available = b.get('qty_available', None)
                incoming_qty = b.get('incoming_qty', None)
                outgoing_qty = b.get('outgoing_qty', None)
                create_date = b.get('create_date', None)

                w_record = {}
                date_ = arrow.get(str(create_date)).datetime

                if id != variant.odoo_id:
                    w_record['odoo_id'] = int(id)
                if name != variant.name:
                    w_record['name'] = name
                if display_name != variant.display_name:
                    w_record['display_name'] = display_name
                if code != variant.code:
                    w_record['code'] = code
                if default_code != variant.default_code:
                    w_record['default_code'] = default_code
                if description != variant.description:
                    w_record['description'] = description
                if bool(active) != variant.active:
                    w_record['active'] = bool(active)
                if int(product_tmpl_id[0]) != variant.product_tmpl_id:
                    w_record['product_tmpl_id'] = int(
                        product_tmpl_id[0])
                if barcode != variant.barcode:
                    w_record['barcode'] = barcode
                if bool(is_product_variant) != variant.is_product_variant:
                    w_record['is_product_variant'] = bool(is_product_variant)
                if bool(available_in_pos) != variant.available_in_pos:
                    w_record['available_in_pos'] = bool(available_in_pos)
                if list(attribute_line_ids) != variant.attribute_line_ids:
                    w_record['attribute_line_ids'] = list(
                        attribute_line_ids)
                if float(price) != variant.price:
                    w_record['price'] = float(price)
                if float(price_extra) != variant.price_extra:
                    w_record['price_extra'] = float(price_extra)
                if float(free_qty) != variant.free_qty:
                    w_record['free_qty'] = float(free_qty)
                if float(qty_available) != variant.qty_available:
                    w_record['qty_available'] = float(qty_available)
                if float(incoming_qty) != variant.incoming_qty:
                    w_record['incoming_qty'] = float(incoming_qty)
                if float(outgoing_qty) != variant.outgoing_qty:
                    w_record['outgoing_qty'] = float(outgoing_qty)
                if date_.replace(tzinfo=None) != variant.created_at:
                    w_record['created_at'] = date_.replace(tzinfo=None)

                if len(w_record) < 1:
                    return resJson(resType.NO_UPD, {})

                setAttr = await updateById(session, ProductVariant, pk_, w_record)
                if not setAttr:
                    resMsg = resType.FAIL_UPD

            return resJson(resMsg, setAttr)
        except:
            exceptionRaise('updateProdVariant')

    @p.patch("/prod-variant")
    @protected
    async def addOrUpdateProdVariant(request):
        try:
            session = request.ctx.session
            body = request.json

            async with session.begin():
                if validate_list(body):
                    body_records = body
                else:
                    body_records = [body]

                # Input validation
                [valid, error] = postProdVariantValidator(body_records)
                if not valid:
                    return resJson(resType.INVALID_PARAMS, error, len(error))

                output_list = []

                [new_list, update_list, redundant_ids] = await insertOrUpdate(session, body_records)
                if new_list:
                    # Post new record
                    result = await insertQuery(session, ProductVariant, new_list)

                    for u in result:
                        output_list.append(u.id)

                if update_list:
                    result = await bulkUpdateQuery(session, ProductVariant, redundant_ids, update_list)

                    for u in result:
                        output_list.append(u)

                if not output_list:
                    return resJson(resType.NO_UPD, {})

            return resJson(resType.OK, output_list, len(output_list))
        except:
            exceptionRaise('addOrUpdateProdVariant')


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
            code = b.get('code', None)
            default_code = b.get('default_code', None)
            description = b.get('description', None)
            active = b.get('active', None)
            product_tmpl_id = b.get('product_tmpl_id', None)
            barcode = b.get('barcode', None)
            if barcode == False:
                barcode = None
            else:
                barcode = str(barcode)

            is_product_variant = b.get('is_product_variant', None)
            available_in_pos = b.get('available_in_pos', None)
            attribute_line_ids = b.get('attribute_line_ids', None)
            price = b.get('price', None)
            price_extra = b.get('price_extra', None)
            free_qty = b.get('free_qty', None)
            qty_available = b.get('qty_available', None)
            incoming_qty = b.get('incoming_qty', None)
            outgoing_qty = b.get('outgoing_qty', None)
            create_date = b.get('create_date', None)
            w_record = {}

            if not bg:
                variant = await findRecordByColumn(session, ProductVariant, ProductVariant.odoo_id, int(id), False)
            else:
                variant = await findRecordByColumnCron(session, ProductVariant, ProductVariant.odoo_id, int(id), False)
            if not variant:
                # register record
                date_ = arrow.get(str(create_date)).datetime
                w_record = {
                    "odoo_id": int(id),
                    "name": str(name),
                    "display_name": str(display_name),
                    "code": str(code),
                    "default_code": str(default_code),
                    "description": str(description),
                    "active": bool(active),
                    "product_tmpl_id": int(product_tmpl_id[0]),
                    "barcode": barcode,
                    "is_product_variant": bool(is_product_variant),
                    "available_in_pos": bool(available_in_pos),
                    "attribute_line_ids": list(attribute_line_ids),
                    "price": float(price),
                    "price_extra": float(price_extra),
                    "free_qty": float(free_qty),
                    "qty_available": float(qty_available),
                    "incoming_qty": float(incoming_qty),
                    "outgoing_qty": float(outgoing_qty),
                    "created_at": date_.replace(tzinfo=None)
                }
                new_list.append(w_record)
            else:
                # update record
                date_ = arrow.get(str(create_date)).datetime

                if name != variant.name:
                    w_record['name'] = name
                if display_name != variant.display_name:
                    w_record['display_name'] = display_name
                if code != variant.code:
                    w_record['code'] = code
                if default_code != variant.default_code:
                    w_record['default_code'] = default_code
                if description != variant.description:
                    w_record['description'] = description
                if bool(active) != variant.active:
                    w_record['active'] = bool(active)
                if int(product_tmpl_id[0]) != variant.product_tmpl_id:
                    w_record['product_tmpl_id'] = int(
                        product_tmpl_id[0])
                if barcode != variant.barcode:
                    w_record['barcode'] = barcode
                if bool(is_product_variant) != variant.is_product_variant:
                    w_record['is_product_variant'] = bool(is_product_variant)
                if bool(available_in_pos) != variant.available_in_pos:
                    w_record['available_in_pos'] = bool(available_in_pos)
                if list(attribute_line_ids) != variant.attribute_line_ids:
                    w_record['attribute_line_ids'] = list(
                        attribute_line_ids)
                if float(price) != variant.price:
                    w_record['price'] = float(price)
                if float(price_extra) != variant.price_extra:
                    w_record['price_extra'] = float(price_extra)
                if float(free_qty) != variant.free_qty:
                    w_record['free_qty'] = float(free_qty)
                if float(qty_available) != variant.qty_available:
                    w_record['qty_available'] = float(qty_available)
                if float(incoming_qty) != variant.incoming_qty:
                    w_record['incoming_qty'] = float(incoming_qty)
                if float(outgoing_qty) != variant.outgoing_qty:
                    w_record['outgoing_qty'] = float(outgoing_qty)
                if date_.replace(tzinfo=None) != variant.created_at:
                    w_record['created_at'] = date_.replace(tzinfo=None)

                if w_record:
                    w_record['odoo_id'] = variant.odoo_id
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
        result = await insertQuery(session, ProductVariant, new_list)

        for u in result:
            output_list.append(u.id)

    if update_list:
        result = await bulkUpdateQuery(session, ProductVariant, redundant_ids, update_list)

        for u in result:
            output_list.append(u)

    if (not output_list) and (not redundant_ids):
        await session.rollback()

    return output_list


# Cron auto feed to db func
async def migrateProdVariantToDB(app):
    async with app.ctx.db.begin() as conn:
        # TODO: async func can await call from odoo, need improvements?
        output = await get_prod_detail_by_id()
        _ = await cronAddUpdateProcess(conn, output)

        await conn.commit()
        await conn.close()
    return True
