from helpers.func import (
    resJson,
    resType,
    exceptionRaise,
    validate_list
)
from helpers.validator import paginateValidator, postProdCategoryValidator, updateProdCategoryValidator
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
from models.product_category import ProductCategory
from utils.auth import protected
from sqlalchemy import update
from odoo.main import get_prod_cat

import arrow

# -----------------
# API Class Section
# -----------------


class ProductCategoryController():
    p = Blueprint('prod_category', url_prefix='/')

    @p.get("/prod-categories")
    @protected
    async def getProdCategories(request):
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
                    ProductCategory.id,
                    ProductCategory.odoo_id,
                    ProductCategory.name,
                    ProductCategory.complete_name,
                    ProductCategory.display_name,
                    ProductCategory.parent_id,
                    ProductCategory.parent_path,
                    ProductCategory.child_id,
                    ProductCategory.product_count,
                    ProductCategory.created_at
                ]

                [stmt, count_] = paginatedQuery(
                    ProductCategory, sort, order, select_items, size, page)
                result = await session.execute(stmt)
                categories = result.all()

                result_dict = [dict(category)
                               for category in categories]
                total_ = await session.execute(count_)
                total = total_.scalar()

            return resJson(resType.OK, result_dict, total)
        except:
            exceptionRaise('getProdCategories')

    @p.get("/prod-category/<pk_:uuid>")
    @protected
    async def getProdCategory(request, pk_):
        try:
            session = request.ctx.session
            async with session.begin():
                category = await findRecordById(session, ProductCategory, pk_)

            if not category:
                return resJson(resType.NO_RECORD)

            return resJson(resType.OK, category.to_dict())
        except:
            exceptionRaise('getProdCategory')

    # MARK: Support scalar and multi input

    @p.post("/prod-category")
    @protected
    async def createProdCategory(request):
        try:
            session = request.ctx.session
            body = request.json

            async with session.begin():
                if validate_list(body):
                    body_records = body
                else:
                    body_records = [body]

                # Input validation
                [valid, error] = postProdCategoryValidator(body_records)
                if not valid:
                    return resJson(resType.INVALID_PARAMS, error, len(error))

                output_list = []

                [new_list, update_list, redundant_ids] = await insertOrUpdate(session, body_records)
                if (not update_list) and (not redundant_ids):
                    # Post new record
                    result = await insertQuery(session, ProductCategory, new_list)
                else:
                    return resJson(resType.DUPLICATE, redundant_ids, len(redundant_ids))

                for u in result:
                    output_list.append(dict(u))

            return resJson(resType.OK, output_list, len(output_list))
        except:
            exceptionRaise('createProdCategory')

    @p.delete("/prod-category/<pk_:uuid>")
    @protected
    async def destroyProdCategory(request, pk_):
        try:
            session = request.ctx.session
            resMsg = resType.SUCCESS_DEL
            async with session.begin():
                category = await findRecordById(session, ProductCategory, pk_)
                if not category:
                    return resJson(resType.NO_RECORD)

                destroy = await softDelbyId(session, ProductCategory, pk_)
                if not destroy:
                    resMsg = resType.FAIL_DELETE

            return resJson(resMsg, destroy)
        except:
            exceptionRaise('destroyProdCategory')

    @p.put("/prod-category/<pk_:uuid>")
    @protected
    async def updateProdCategory(request, pk_):
        try:
            session = request.ctx.session
            b = request.json
            # Input validation
            [valid, error] = updateProdCategoryValidator(b)
            if not valid:
                return resJson(resType.INVALID_PARAMS, error, len(error))

            resMsg = resType.SUCCESS_UPD
            async with session.begin():
                category = await findRecordById(session, ProductCategory, pk_)
                if not category:
                    return resJson(resType.NO_RECORD)

                id = b.get('id', None)
                name = b.get('name', None)
                complete_name = b.get('complete_name', None)
                display_name = b.get('display_name', None)
                parent_id = b.get('parent_id', None)
                if parent_id == False:
                    parent_id = None
                else:
                    parent_id = int(parent_id[0])

                parent_path = b.get('parent_path', None)
                child_id = b.get('child_id', None)
                product_count = b.get('product_count', None)
                create_date = b.get('create_date', None)

                w_record = {}
                date_ = arrow.get(str(create_date)).datetime

                if id != category.odoo_id:
                    w_record['odoo_id'] = int(id)
                if name != category.name:
                    w_record['name'] = name
                if complete_name != category.complete_name:
                    w_record['complete_name'] = complete_name
                if display_name != category.display_name:
                    w_record['display_name'] = display_name
                if parent_id != category.parent_id:
                    w_record['parent_id'] = parent_id
                if parent_path != category.parent_path:
                    w_record['parent_path'] = parent_path
                if list(child_id) != category.child_id:
                    w_record['child_id'] = list(child_id)
                if int(product_count) != category.product_count:
                    w_record['product_count'] = int(product_count)
                if date_.replace(tzinfo=None) != category.created_at:
                    w_record['created_at'] = date_.replace(tzinfo=None)

                if len(w_record) < 1:
                    return resJson(resType.NO_UPD, {})

                setAttr = await updateById(session, ProductCategory, pk_, w_record)
                if not setAttr:
                    resMsg = resType.FAIL_UPD

            return resJson(resMsg, setAttr)
        except:
            exceptionRaise('updateProdCategory')

    @p.patch("/prod-category")
    @protected
    async def addOrUpdateProdCategory(request):
        try:
            session = request.ctx.session
            body = request.json

            async with session.begin():
                if validate_list(body):
                    body_records = body
                else:
                    body_records = [body]

                # Input validation
                [valid, error] = postProdCategoryValidator(body_records)
                if not valid:
                    return resJson(resType.INVALID_PARAMS, error, len(error))

                output_list = []

                [new_list, update_list, redundant_ids] = await insertOrUpdate(session, body_records)
                if new_list:
                    # Post new record
                    result = await insertQuery(session, ProductCategory, new_list)

                    for u in result:
                        output_list.append(u.id)

                if update_list:
                    result = await bulkUpdateQuery(session, ProductCategory, redundant_ids, update_list)

                    for u in result:
                        output_list.append(u)

                if not output_list:
                    return resJson(resType.NO_UPD, {})

            return resJson(resType.OK, output_list, len(output_list))
        except:
            exceptionRaise('addOrUpdateProdCategory')


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
            complete_name = b.get('complete_name', None)
            display_name = b.get('display_name', None)
            parent_id = b.get('parent_id', None)
            if parent_id == False:
                parent_id = None
            else:
                parent_id = int(parent_id[0])

            parent_path = b.get('parent_path', None)
            child_id = b.get('child_id', None)
            product_count = b.get('product_count', None)
            create_date = b.get('create_date', None)
            w_record = {}

            if not bg:
                category = await findRecordByColumn(session, ProductCategory, ProductCategory.odoo_id, int(id), False)
            else:
                category = await findRecordByColumnCron(session, ProductCategory, ProductCategory.odoo_id, int(id), False)
            if not category:
                # register record
                date_ = arrow.get(str(create_date)).datetime
                w_record = {
                    "odoo_id": int(id),
                    "name": str(name),
                    "complete_name": str(complete_name),
                    "display_name": str(display_name),
                    "parent_id": parent_id,
                    "parent_path": str(parent_path),
                    "child_id": list(child_id),
                    "product_count": int(product_count),
                    "created_at": date_.replace(tzinfo=None)
                }
                new_list.append(w_record)
            else:
                # update record
                date_ = arrow.get(str(create_date)).datetime

                if name != category.name:
                    w_record['name'] = name
                if complete_name != category.complete_name:
                    w_record['complete_name'] = complete_name
                if display_name != category.display_name:
                    w_record['display_name'] = display_name
                if parent_id != category.parent_id:
                    w_record['parent_id'] = parent_id
                if parent_path != category.parent_path:
                    w_record['parent_path'] = parent_path
                if list(child_id) != category.child_id:
                    w_record['child_id'] = list(child_id)
                if int(product_count) != category.product_count:
                    w_record['product_count'] = int(product_count)
                if date_.replace(tzinfo=None) != category.created_at:
                    w_record['created_at'] = date_.replace(tzinfo=None)

                if w_record:
                    w_record['odoo_id'] = category.odoo_id
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
        result = await insertQuery(session, ProductCategory, new_list)

        for u in result:
            output_list.append(u.id)

    if update_list:
        result = await bulkUpdateQuery(session, ProductCategory, redundant_ids, update_list)

        for u in result:
            output_list.append(u)

    if (not output_list) and (not redundant_ids):
        await session.rollback()

    return output_list


# Cron auto feed to db func
async def migrateProdCategoryToDB(app):
    async with app.ctx.db.begin() as conn:
        # TODO: async func can await call from odoo, need improvements?
        output = await get_prod_cat()
        _ = await cronAddUpdateProcess(conn, output)

        await conn.commit()
        await conn.close()
    return True
