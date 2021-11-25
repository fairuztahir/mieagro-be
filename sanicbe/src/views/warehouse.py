from helpers.helpers import (
    resJson,
    resType,
    exceptionRaise,
    capitalName,
    validate_list,
    capitalSentence,
    invertBool,
    listRemoveIf,
    count_list,
    find_duplicate,
    set_dict
)
from helpers.validator import paginateValidator, postWarehouseValidator, updateWarehouseValidator
from utils.utils import (
    paginatedQuery,
    insertQuery,
    softDelbyId,
    findRecordById,
    findRecordByColumn,
    updateById
)
from sanic.log import logger
from sanic import Blueprint
from models.warehouse import Warehouse
from utils.auth import protected
from sqlalchemy import update

import moment

# -----------------
# API Class Section
# -----------------


class WarehouseController():
    wh = Blueprint('warehouse', url_prefix='/')

    @wh.get("/warehouses")
    @protected
    async def getWarehouse(request):
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
                    Warehouse.id,
                    Warehouse.odoo_id,
                    Warehouse.code,
                    Warehouse.name,
                    Warehouse.display_name,
                    Warehouse.active,
                    Warehouse.reception_steps,
                    Warehouse.delivery_steps,
                    Warehouse.description,
                    Warehouse.created_at
                ]

                [stmt, count_] = paginatedQuery(
                    Warehouse, sort, order, select_items, size, page)
                result = await session.execute(stmt)
                roles = result.all()

                result_dict = [dict(role) for role in roles]
                total_ = await session.execute(count_)
                total = total_.scalar()

            return resJson(resType.OK, result_dict, total)
        except:
            exceptionRaise('getWarehouse')

    @wh.get("/warehouse/<pk_:uuid>")
    @protected
    async def getWarehouse(request, pk_):
        try:
            session = request.ctx.session
            async with session.begin():
                warehouse = await findRecordById(session, Warehouse, pk_)

            if not warehouse:
                return resJson(resType.NO_RECORD)

            return resJson(resType.OK, warehouse.to_dict())
        except:
            exceptionRaise('getWarehouse')

    # MARK: Support scalar and multi input

    @wh.post("/warehouse")
    @protected
    async def createWarehouse(request):
        try:
            session = request.ctx.session
            body = request.json

            async with session.begin():
                if validate_list(body):
                    body_records = body
                else:
                    body_records = [body]

                # Input validation
                [valid, error] = postWarehouseValidator(body_records)
                if not valid:
                    return resJson(resType.INVALID_PARAMS, error, len(error))

                output_list = []

                [new_list, update_list, redundant_ids] = await insertOrUpdate(session, body_records)
                if (not update_list) and (not redundant_ids):
                    # Post new record
                    result = await insertQuery(session, Warehouse, new_list)
                else:
                    return resJson(resType.DUPLICATE, redundant_ids, len(redundant_ids))

                for u in result:
                    output_list.append(dict(u))

            return resJson(resType.OK, output_list, len(output_list))
        except:
            exceptionRaise('createWarehouse')

    @wh.delete("/warehouse/<pk_:uuid>")
    @protected
    async def destroyWarehouse(request, pk_):
        try:
            session = request.ctx.session
            resMsg = resType.SUCCESS_DEL
            async with session.begin():
                warehouse = await findRecordById(session, Warehouse, pk_)
                if not warehouse:
                    return resJson(resType.NO_RECORD)

                destroy = await softDelbyId(session, Warehouse, pk_)
                if not destroy:
                    resMsg = resType.FAIL_DELETE

            return resJson(resMsg, destroy)
        except:
            exceptionRaise('destroyWarehouse')

    @wh.put("/warehouse/<pk_:uuid>")
    @protected
    async def updateWarehouse(request, pk_):
        try:
            session = request.ctx.session
            b = request.json
            # Input validation
            [valid, error] = updateWarehouseValidator(b)
            if not valid:
                return resJson(resType.INVALID_PARAMS, error, len(error))

            resMsg = resType.SUCCESS_UPD
            async with session.begin():
                warehouse_ = await findRecordById(session, Warehouse, pk_)
                if not warehouse_:
                    return resJson(resType.NO_RECORD)

                id = b.get('id', None)
                code = b.get('code', None)
                name = b.get('name', None)
                display_name = b.get('display_name', None)
                active = b.get('active', None)
                reception_steps = b.get('reception_steps', None)
                delivery_steps = b.get('delivery_steps', None)
                create_date = b.get('create_date', None)

                values_ = {}
                if id != warehouse_.odoo_id:
                    values_['odoo_id'] = int(id)
                if code != warehouse_.code:
                    values_['code'] = code
                if name != warehouse_.name:
                    values_['name'] = name
                if display_name != warehouse_.display_name:
                    values_['display_name'] = display_name
                if bool(active) != warehouse_.active:
                    values_['active'] = bool(active)
                if reception_steps != warehouse_.reception_steps:
                    values_['reception_steps'] = reception_steps
                if delivery_steps != warehouse_.delivery_steps:
                    values_['delivery_steps'] = delivery_steps
                if moment.date(str(create_date)).date != warehouse_.created_at:
                    values_['created_at'] = moment.date(
                        str(create_date)).date

                if len(values_) < 1:
                    return resJson(resType.NO_UPD, {})

                setWarehouse_ = await updateById(session, Warehouse, pk_, values_)
                if not setWarehouse_:
                    resMsg = resType.FAIL_UPD

            return resJson(resMsg, setWarehouse_)
        except:
            exceptionRaise('updateWarehouse')

    @wh.patch("/warehouse")
    @protected
    async def addOrUpdateWarehouse(request):
        try:
            session = request.ctx.session
            body = request.json

            async with session.begin():
                if validate_list(body):
                    body_records = body
                else:
                    body_records = [body]

                # Input validation
                [valid, error] = postWarehouseValidator(body_records)
                if not valid:
                    return resJson(resType.INVALID_PARAMS, error, len(error))

                output_list = []

                [new_list, update_list, redundant_ids] = await insertOrUpdate(session, body_records)
                if new_list:
                    # Post new record
                    result = await insertQuery(session, Warehouse, new_list)

                    for u in result:
                        output_list.append(u.id)

                if update_list:
                    result = await bulkUpdateQuery(session, Warehouse, redundant_ids, update_list)

                    for u in result:
                        output_list.append(u)

                if not output_list:
                    return resJson(resType.NO_UPD, {})

            return resJson(resType.OK, output_list, len(output_list))
        except:
            exceptionRaise('addOrUpdateWarehouse')


# -----------------
# functions section
# -----------------
async def insertOrUpdate(session, body):
    try:
        new_list, update_list, redundant_ids = [], [], []
        for b in body:
            id = b.get('id', None)
            code = b.get('code', None)
            name = b.get('name', None)
            display_name = b.get('display_name', None)
            active = b.get('active', None)
            reception_steps = b.get('reception_steps', None)
            delivery_steps = b.get('delivery_steps', None)
            create_date = b.get('create_date', None)
            w_record = {}

            warehouse = await findRecordByColumn(session, Warehouse, Warehouse.odoo_id, int(id), False)
            if not warehouse:
                # register record
                w_record = {
                    "odoo_id": int(id),
                    "code": str(code),
                    "name": str(name),
                    "display_name": str(display_name),
                    "active": bool(active),
                    "reception_steps": str(reception_steps),
                    "delivery_steps": str(delivery_steps),
                    "created_at": moment.date(str(create_date)).date
                }
                new_list.append(w_record)
            else:
                # update record
                if code != warehouse['code']:
                    w_record['code'] = code
                if name != warehouse['name']:
                    w_record['name'] = name
                if display_name != warehouse['display_name']:
                    w_record['display_name'] = display_name
                if bool(active) != warehouse['active']:
                    w_record['active'] = bool(active)
                if reception_steps != warehouse['reception_steps']:
                    w_record['reception_steps'] = reception_steps
                if delivery_steps != warehouse['delivery_steps']:
                    w_record['delivery_steps'] = delivery_steps
                if moment.date(str(create_date)).date != warehouse['created_at']:
                    w_record['created_at'] = moment.date(
                        str(create_date)).date

                if w_record:
                    w_record['odoo_id'] = warehouse['odoo_id']
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
