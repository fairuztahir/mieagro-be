from helpers.func import (
    resJson,
    resType,
    exceptionRaise,
    validate_list
)
from helpers.validator import paginateValidator, postProductValidator, updateProductValidator
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
from models.product import Product
from utils.auth import protected
from sqlalchemy import update
from odoo.main import get_prod_temp

import arrow

# -----------------
# API Class Section
# -----------------


class ProductController():
    p = Blueprint('product', url_prefix='/')

    @p.get("/products")
    @protected
    async def getProducts(request):
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
                    Product.id,
                    Product.odoo_id,
                    Product.code,
                    Product.name,
                    Product.display_name,
                    Product.active,
                    Product.available_in_pos,
                    Product.uom_name,
                    Product.template_price,
                    Product.template_list_price,
                    Product.template_cost_price,
                    Product.product_variant_count,
                    Product.product_variant_ids,
                    Product.barcode,
                    Product.qty_available,
                    Product.incoming_qty,
                    Product.outgoing_qty,
                    Product.description,
                    Product.created_at
                ]

                [stmt, count_] = paginatedQuery(
                    Product, sort, order, select_items, size, page)
                result = await session.execute(stmt)
                products = result.all()

                result_dict = [dict(product) for product in products]
                total_ = await session.execute(count_)
                total = total_.scalar()

            return resJson(resType.OK, result_dict, total)
        except:
            exceptionRaise('getProducts')

    @p.get("/product/<pk_:uuid>")
    @protected
    async def getProduct(request, pk_):
        try:
            session = request.ctx.session
            async with session.begin():
                product = await findRecordById(session, Product, pk_)

            if not product:
                return resJson(resType.NO_RECORD)

            return resJson(resType.OK, product.to_dict())
        except:
            exceptionRaise('getProduct')

    # MARK: Support scalar and multi input

    @p.post("/product")
    @protected
    async def createProduct(request):
        try:
            session = request.ctx.session
            body = request.json

            async with session.begin():
                if validate_list(body):
                    body_records = body
                else:
                    body_records = [body]

                # Input validation
                [valid, error] = postProductValidator(body_records)
                if not valid:
                    return resJson(resType.INVALID_PARAMS, error, len(error))

                output_list = []

                [new_list, update_list, redundant_ids] = await insertOrUpdate(session, body_records)
                if (not update_list) and (not redundant_ids):
                    # Post new record
                    result = await insertQuery(session, Product, new_list)
                else:
                    return resJson(resType.DUPLICATE, redundant_ids, len(redundant_ids))

                for u in result:
                    output_list.append(dict(u))

            return resJson(resType.OK, output_list, len(output_list))
        except:
            exceptionRaise('createProduct')

    @p.delete("/product/<pk_:uuid>")
    @protected
    async def destroyProduct(request, pk_):
        try:
            session = request.ctx.session
            resMsg = resType.SUCCESS_DEL
            async with session.begin():
                product = await findRecordById(session, Product, pk_)
                if not product:
                    return resJson(resType.NO_RECORD)

                destroy = await softDelbyId(session, Product, pk_)
                if not destroy:
                    resMsg = resType.FAIL_DELETE

            return resJson(resMsg, destroy)
        except:
            exceptionRaise('destroyWarehouse')

    @p.put("/product/<pk_:uuid>")
    @protected
    async def updateProduct(request, pk_):
        try:
            session = request.ctx.session
            b = request.json
            # Input validation
            [valid, error] = updateProductValidator(b)
            if not valid:
                return resJson(resType.INVALID_PARAMS, error, len(error))

            resMsg = resType.SUCCESS_UPD
            async with session.begin():
                product = await findRecordById(session, Product, pk_)
                if not product:
                    return resJson(resType.NO_RECORD)

                id = b.get('id', None)
                code = b.get('default_code', None)
                name = b.get('name', None)
                display_name = b.get('display_name', None)
                active = b.get('active', None)
                available_in_pos = b.get('available_in_pos', None)
                uom_name = b.get('uom_name', None)
                template_price = b.get('price', None)
                template_list_price = b.get('list_price', None)
                template_cost_price = b.get('standard_price', None)
                product_variant_count = b.get('product_variant_count', None)
                product_variant_ids = b.get('product_variant_ids', None)
                barcode = b.get('barcode', None)
                qty_available = b.get('qty_available', None)
                incoming_qty = b.get('incoming_qty', None)
                outgoing_qty = b.get('outgoing_qty', None)
                description = b.get('description', None)
                create_date = b.get('create_date', None)

                w_record = {}
                date_ = arrow.get(str(create_date)).datetime

                # Condition if value is bool False (empty)
                if not code:
                    code = None
                else:
                    code = str(code)

                if not barcode:
                    barcode = None
                else:
                    barcode = str(barcode)

                if id != product.odoo_id:
                    w_record['odoo_id'] = int(id)
                if code != product.code:
                    w_record['code'] = code
                if name != product.name:
                    w_record['name'] = name
                if display_name != product.display_name:
                    w_record['display_name'] = display_name
                if bool(active) != product.active:
                    w_record['active'] = bool(active)
                if bool(available_in_pos) != product.available_in_pos:
                    w_record['available_in_pos'] = bool(available_in_pos)
                if uom_name != product.uom_name:
                    w_record['uom_name'] = uom_name
                if float(template_price) != product.template_price:
                    w_record['template_price'] = float(template_price)
                if float(template_list_price) != product.template_list_price:
                    w_record['template_list_price'] = float(
                        template_list_price)
                if float(template_cost_price) != product.template_cost_price:
                    w_record['template_cost_price'] = float(
                        template_cost_price)
                if int(product_variant_count) != product.product_variant_count:
                    w_record['product_variant_count'] = int(
                        product_variant_count)
                if list(product_variant_ids) != product.product_variant_ids:
                    w_record['product_variant_ids'] = list(product_variant_ids)
                if barcode != product.barcode:
                    w_record['barcode'] = barcode
                if float(qty_available) != product.qty_available:
                    w_record['qty_available'] = float(qty_available)
                if float(incoming_qty) != product.incoming_qty:
                    w_record['incoming_qty'] = float(incoming_qty)
                if float(outgoing_qty) != product.outgoing_qty:
                    w_record['outgoing_qty'] = float(outgoing_qty)
                if description != product.description:
                    w_record['description'] = description
                if date_.replace(tzinfo=None) != product.created_at:
                    w_record['created_at'] = date_.replace(tzinfo=None)

                if len(w_record) < 1:
                    return resJson(resType.NO_UPD, {})

                setProduct = await updateById(session, Product, pk_, w_record)
                if not setProduct:
                    resMsg = resType.FAIL_UPD

            return resJson(resMsg, setProduct)
        except:
            exceptionRaise('updateProduct')

    @p.patch("/product")
    @protected
    async def addOrUpdateProduct(request):
        try:
            session = request.ctx.session
            body = request.json

            async with session.begin():
                if validate_list(body):
                    body_records = body
                else:
                    body_records = [body]

                # Input validation
                [valid, error] = postProductValidator(body_records)
                if not valid:
                    return resJson(resType.INVALID_PARAMS, error, len(error))

                output_list = []

                [new_list, update_list, redundant_ids] = await insertOrUpdate(session, body_records)
                if new_list:
                    # Post new record
                    result = await insertQuery(session, Product, new_list)

                    for u in result:
                        output_list.append(u.id)

                if update_list:
                    result = await bulkUpdateQuery(session, Product, redundant_ids, update_list)

                    for u in result:
                        output_list.append(u)

                if not output_list:
                    return resJson(resType.NO_UPD, {})

            return resJson(resType.OK, output_list, len(output_list))
        except:
            exceptionRaise('addOrUpdateProduct')


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
            code = b.get('default_code', None)
            name = b.get('name', None)
            display_name = b.get('display_name', None)
            active = b.get('active', None)
            available_in_pos = b.get('available_in_pos', None)
            uom_name = b.get('uom_name', None)
            template_price = b.get('price', None)
            template_list_price = b.get('list_price', None)
            template_cost_price = b.get('standard_price', None)
            product_variant_count = b.get('product_variant_count', None)
            product_variant_ids = b.get('product_variant_ids', None)
            barcode = b.get('barcode', None)
            qty_available = b.get('qty_available', None)
            incoming_qty = b.get('incoming_qty', None)
            outgoing_qty = b.get('outgoing_qty', None)
            description = b.get('description', None)
            create_date = b.get('create_date', None)
            w_record = {}
            # Condition if value is bool False (empty)
            if not code:
                code = None
            else:
                code = str(code)

            if not barcode:
                barcode = None
            else:
                barcode = str(barcode)

            if not bg:
                product = await findRecordByColumn(session, Product, Product.odoo_id, int(id), False)
            else:
                product = await findRecordByColumnCron(session, Product, Product.odoo_id, int(id), False)
            if not product:
                # register record
                date_ = arrow.get(str(create_date)).datetime
                w_record = {
                    "odoo_id": int(id),
                    "code": code,
                    "name": str(name),
                    "display_name": str(display_name),
                    "active": bool(active),
                    "available_in_pos": bool(available_in_pos),
                    "uom_name": str(uom_name),
                    "template_price": float(template_price),
                    "template_list_price": float(template_list_price),
                    "template_cost_price": float(template_cost_price),
                    "product_variant_count": int(product_variant_count),
                    "product_variant_ids": list(product_variant_ids),
                    "barcode": barcode,
                    "qty_available": float(qty_available),
                    "incoming_qty": float(incoming_qty),
                    "outgoing_qty": float(outgoing_qty),
                    "description": str(description),
                    "created_at": date_.replace(tzinfo=None)
                }
                new_list.append(w_record)
            else:
                # update record
                date_ = arrow.get(str(create_date)).datetime

                if code != product.code:
                    w_record['code'] = code
                if name != product.name:
                    w_record['name'] = name
                if display_name != product.display_name:
                    w_record['display_name'] = display_name
                if bool(active) != product.active:
                    w_record['active'] = bool(active)
                if bool(available_in_pos) != product.available_in_pos:
                    w_record['available_in_pos'] = bool(available_in_pos)
                if uom_name != product.uom_name:
                    w_record['uom_name'] = uom_name
                if float(template_price) != product.template_price:
                    w_record['template_price'] = float(template_price)
                if float(template_list_price) != product.template_list_price:
                    w_record['template_list_price'] = float(
                        template_list_price)
                if float(template_cost_price) != product.template_cost_price:
                    w_record['template_cost_price'] = float(
                        template_cost_price)
                if int(product_variant_count) != product.product_variant_count:
                    w_record['product_variant_count'] = int(
                        product_variant_count)
                if list(product_variant_ids) != product.product_variant_ids:
                    w_record['product_variant_ids'] = list(product_variant_ids)
                if barcode != product.barcode:
                    w_record['barcode'] = barcode
                if float(qty_available) != product.qty_available:
                    w_record['qty_available'] = float(qty_available)
                if float(incoming_qty) != product.incoming_qty:
                    w_record['incoming_qty'] = float(incoming_qty)
                if float(outgoing_qty) != product.outgoing_qty:
                    w_record['outgoing_qty'] = float(outgoing_qty)
                if description != product.description:
                    w_record['description'] = description
                if date_.replace(tzinfo=None) != product.created_at:
                    w_record['created_at'] = date_.replace(tzinfo=None)

                if w_record:
                    w_record['odoo_id'] = product.odoo_id
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
        result = await insertQuery(session, Product, new_list)

        for u in result:
            output_list.append(u.id)

    if update_list:
        result = await bulkUpdateQuery(session, Product, redundant_ids, update_list)

        for u in result:
            output_list.append(u)

    if (not output_list) and (not redundant_ids):
        await session.rollback()

    return output_list


# Cron auto feed to db func
async def migrateProductToDB(app):
    async with app.ctx.db.begin() as conn:
        # TODO: async func can await call from odoo, need improvements?
        output = await get_prod_temp()
        _ = await cronAddUpdateProcess(conn, output)

        await conn.commit()
        await conn.close()
    return True
