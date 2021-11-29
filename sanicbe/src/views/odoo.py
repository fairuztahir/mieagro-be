from datetime import datetime
from sanic.log import logger
from sanic import Blueprint
from utils.auth import protected
from utils.exportcsv import DownloadCSVView
from helpers.func import (
    resJson,
    resType,
    exceptionRaise,
    count_loop_page
)
from odoo.main import (
    get_all_warehouse,
    get_prod_temp,
    get_pos_order,
    get_prod_detail_by_id,
    set_pos_order,
    get_pos_order_line
)


class OdooController():
    o = Blueprint('odoo', url_prefix='/odoo')

    @o.get("/warehouses")
    @protected
    async def getWarehouses(request):
        try:
            session = request.ctx.session
            params = request.args
            async with session.begin():
                [result, count] = await get_all_warehouse()

            return resJson(resType.OK, result, count)
        except:
            exceptionRaise('getWarehouses')

    @o.get("/products")
    @protected
    async def getProducts(request):
        try:
            session = request.ctx.session
            params = request.args

            async with session.begin():
                size = int(params.get('pageSize', 10))
                page = int(params.get('page', 1))
                [result, count] = await get_prod_temp(page, size)

                for u in result:
                    if u['product_variant_count']:
                        subpage = 1
                        size_ = len(u['product_variant_ids'])
                        [get_variants, count_variant] = await get_prod_detail_by_id(u['product_variant_ids'], subpage, size_)

                        u['product_variant_details'] = get_variants

            return resJson(resType.OK, result, count)
        except:
            exceptionRaise('getProducts')

    @o.get("/product-template")
    @protected
    async def getProductTemplate(request):
        try:
            session = request.ctx.session
            params = request.args
            async with session.begin():
                size = int(params.get('pageSize', 10))
                page = int(params.get('page', 1))
                [result, count] = await get_prod_temp(page, size)

            return resJson(resType.OK, result, count)
        except:
            exceptionRaise('getProductTemplate')

    @o.post("/product-variants")
    @protected
    async def getProductVariants(request):
        try:
            session = request.ctx.session
            body = request.json
            async with session.begin():
                size = int(body.get('pageSize', 10))
                page = int(body.get('page', 1))
                variants = list(body.get('ids', []))
                [result, count] = await get_prod_detail_by_id(variants, page, size)

            return resJson(resType.OK, result, count)
        except:
            exceptionRaise('getProductVariants')

    @o.get("/pos-order")
    @protected
    async def getPOSOrder(request):
        try:
            session = request.ctx.session
            params = request.args
            async with session.begin():
                size = int(params.get('pageSize', 10))
                page = int(params.get('page', 1))
                date = params.get('to_date', None)

                # [result, count] = await get_pos_order(page, size, date)
                [result, count] = await set_pos_order(date)

            return resJson(resType.OK, result, count)
        except:
            exceptionRaise('getPOSOrder')

    @o.get("/pos-order-line")
    @protected
    async def getPOSOrderLine(request):
        try:
            session = request.ctx.session
            params = request.args
            async with session.begin():
                size = int(params.get('pageSize', 10))
                page = int(params.get('page', 1))
                date = params.get('to_date', None)
                orderId = int(params.get('orderId', 0))

                # [result, count] = await get_pos_order(page, size, date)
                [result, count] = await get_pos_order_line(date, orderId)

            return resJson(resType.OK, result, count)
        except:
            exceptionRaise('getPOSOrderLine')


# -----------------
# functions section
# -----------------
async def get_export_order():
    [result, count] = await set_pos_order()
    # await DownloadCSVView.get()
    print('export', count)
    return True
