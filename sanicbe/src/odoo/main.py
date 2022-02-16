import xmlrpc.client
import arrow
import os

from helpers.func import valueOf, set_dict
from zoneinfo import ZoneInfo
from datetime import datetime

HOST = os.getenv('ODOO_HOST', 'localhost')
DB = os.getenv('ODOO_DB', 'mieagro')
USER = os.getenv('ODOO_USER', 'fairuztahir@gmail.com')
PWD = os.getenv('ODOO_PWD', 'secret')

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(HOST))
uid = common.authenticate(DB, USER, PWD, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(HOST))


# Get Odoo version
async def get_version():
    return common.version()


# Check access rights
async def access_status():
    return models.execute_kw(DB, uid, PWD,
                             'res.partner', 'check_access_rights',
                             ['read'], {'raise_exception': False})


# Search partner details
async def search_partner():
    return models.execute_kw(DB, uid, PWD,
                             'res.partner', 'search',
                             [[['is_company', '=', True]]],
                             {'offset': 0, 'limit': 5})


# return product/variant details by ids = []
async def get_prod_detail_by_id(ids=[]):
    if not ids:
        condition = ['id', '>', 0]
    else:
        condition = ['id', 'in', ids]

    output = models.execute_kw(DB, uid, PWD,
                               'product.product', 'search_read',
                               [[condition]],
                               {'fields': [
                                   'code',
                                   'default_code',
                                   'name',
                                   'display_name',
                                   'description',
                                   'active',
                                   'product_tmpl_id',
                                   'barcode',
                                   'is_product_variant',
                                   'available_in_pos',
                                   'attribute_line_ids',
                                   'price',
                                   'price_extra',
                                   'free_qty',
                                   'qty_available',
                                   'incoming_qty',
                                   'outgoing_qty',
                                   'create_date',
                                   'create_uid'
                               ]})

    output.sort(reverse=False, key=lambda e: e['id'])
    return output


# Warehouse Info
# return search detail products
async def get_all_warehouse():
    output = models.execute_kw(DB, uid, PWD,
                               'stock.warehouse',
                               'search_read',
                               [[['active', '=', True]]],
                               {'fields': [
                                   'code',
                                   'name',
                                   'display_name',
                                   'active',
                                   'reception_steps',
                                   'delivery_steps',
                                   'create_date',
                                   'create_uid'
                               ]})

    output.sort(reverse=False, key=lambda e: e['id'])
    return output


# Product Template
# Search product template main class
async def get_prod_temp():
    output = models.execute_kw(DB, uid, PWD,
                               'product.template',
                               'search_read',
                               [[['active', '=', True]]],
                               {'fields': [
                                   'default_code',
                                   'name',
                                   'display_name',
                                   'description',
                                   'categ_id',
                                   'uom_name',
                                   'active',
                                   'available_in_pos',
                                   'price',
                                   'list_price',
                                   'standard_price',
                                   'product_variant_count',
                                   'product_variant_ids',
                                   'barcode',
                                   'qty_available',
                                   'incoming_qty',
                                   'outgoing_qty',
                                   'create_date',
                                   'create_uid'
                               ]})

    output.sort(reverse=False, key=lambda e: e['id'])
    return output


# Product Attributes
# Search product attribute class
async def get_attr(ids=[]):
    if not ids:
        condition = ['id', '>', 0]
    else:
        condition = ['id', 'in', ids]

    output = models.execute_kw(DB, uid, PWD,
                               'product.attribute',
                               'search_read',
                               [[condition]],
                               {'fields': [
                                   'name',
                                   'display_name',
                                   'value_ids',
                                   'attribute_line_ids',
                                   # 'is_used_on_products', deprecated in v15
                                   'product_tmpl_ids',
                                   'create_date'
                               ]})

    output.sort(reverse=False, key=lambda e: e['id'])
    return output


# Search product attribute value
async def get_attr_value(ids=[]):
    if not ids:
        condition = ['id', '>', 0]
    else:
        condition = ['id', 'in', ids]

    output = models.execute_kw(DB, uid, PWD,
                               'product.attribute.value',
                               'search_read',
                               [[condition]],
                               {'fields': [
                                   'name',
                                   'display_name',
                                   'attribute_id',
                                   'pav_attribute_line_ids',
                                   'is_used_on_products',
                                   'create_date'
                               ]})

    output.sort(reverse=False, key=lambda e: e['id'])
    return output


# Search product template attribute line
async def get_prod_attr_line(ids=[]):
    if not ids:
        condition = ['id', '>', 0]
    else:
        condition = ['id', 'in', ids]

    output = models.execute_kw(DB, uid, PWD,
                               'product.template.attribute.line',
                               'search_read',
                               [[condition]],
                               {'fields': [
                                   'display_name',
                                   'active',
                                   'product_tmpl_id',
                                   'attribute_id',
                                   'value_ids',
                                   'product_template_value_ids',
                                   'create_date'
                               ]})

    output.sort(reverse=False, key=lambda e: e['id'])
    return output


# Search product template attribute value
async def get_prod_attr_value(ids=[]):
    if not ids:
        condition = ['id', '>', 0]
    else:
        condition = ['id', 'in', ids]

    output = models.execute_kw(DB, uid, PWD,
                               'product.template.attribute.value',
                               'search_read',
                               [[condition]],
                               {'fields': [
                                   'ptav_active',
                                   'name',
                                   'display_name',
                                   'product_attribute_value_id',
                                   'attribute_line_id',
                                   'price_extra',
                                   'exclude_for',
                                   'product_tmpl_id',
                                   'attribute_id',
                                   'ptav_product_variant_ids',
                                   'is_custom',
                                   'display_type',
                                   'create_date'
                               ]})

    output.sort(reverse=False, key=lambda e: e['id'])
    return output


# TODO: lek luu
# POS
async def get_pos_sale_report(offset=0, limit=10, count=0):
    offset = await offset_correction(offset)
    if count == 0:
        count = models.execute_kw(DB, uid, PWD,
                                  'account.invoice.report',
                                  'search_count',
                                  [[['id', '>', 0]]])

    output = models.execute_kw(DB, uid, PWD,
                               'account.invoice.report',
                               'search_read',
                               [[['id', '>', 0]]])

    return [output, count]


# POS
# TODO: date_order, create_date not local time, UTC
async def get_pos_order(offset=0, limit=10, date=None, count=0):
    offset = await offset_correction(offset)
    [start_from, end_to] = await converto(date)

    if count == 0:
        count = models.execute_kw(DB, uid, PWD,
                                  'pos.order',
                                  'search_count',
                                  [[['date_order', '<=', end_to] and ['date_order', '>=', start_from]]])

    output = models.execute_kw(DB, uid, PWD,
                               'pos.order',
                               'search_read',
                               [[['date_order', '<=', end_to]
                                 and ['date_order', '>=', start_from]]],
                               {'fields': [
                                   'name',
                                   'date_order',
                                   'user_id',
                                   'amount_tax',
                                   'amount_total',
                                   'amount_paid',
                                   'amount_return',
                                   'session_id',
                                   'pos_reference',
                                   'state',
                                   'is_invoiced',
                                   'account_move',
                                   'is_tipped',
                                   'tip_amount',
                                   'loyalty_points',
                                   'sale_journal',
                                   'create_date',
                                   'create_uid'
                               ], 'offset': offset, 'limit': limit})

    [DATAS, COUNT_] = await massage_date_filter(output, start_from, end_to, count)
    return [DATAS, COUNT_]


# POS -- using as main in API and cron, not get_pos_order
# MARK: date_order, create_date not local time, UTC
# MARK: Cronjob processing, paganination not working
async def set_pos_order(date=None):
    [start_from, end_to] = await converto(date)

    count = models.execute_kw(DB, uid, PWD,
                              'pos.order',
                              'search_count',
                              [[['date_order', '<=', end_to] and ['date_order', '>=', start_from]]])

    output = models.execute_kw(DB, uid, PWD,
                               'pos.order',
                               'search_read',
                               [[['date_order', '<=', end_to]
                                 and ['date_order', '>=', start_from]]],
                               {'fields': [
                                   'name',
                                   'date_order',
                                   'user_id',
                                   'config_id',
                                   'amount_tax',
                                   'amount_total',
                                   'amount_paid',
                                   'amount_return',
                                   'session_id',
                                   'pos_reference',
                                   'state',
                                   'is_invoiced',
                                   'account_move',
                                   'is_tipped',
                                   'tip_amount',
                                   'loyalty_points',
                                   'sale_journal',
                                   'create_date',
                                   'create_uid'
                               ], 'offset': 0, 'limit': count})

    [DATAS, COUNT_] = await massage_date_filter(output, start_from, end_to, count)
    return [DATAS, COUNT_]


# return POS order line with discount and products detail
async def get_pos_order_line(date=None, orderId=0):
    [start_from, end_to] = await converto(date)
    searchArr = [['create_date', '<=', end_to]
                 and ['create_date', '>=', start_from]]
    if orderId != 0:
        searchArr.append(['order_id', '=', orderId])

    count = models.execute_kw(DB, uid, PWD,
                              'pos.order.line',
                              'search_count',
                              [searchArr])

    output = models.execute_kw(DB, uid, PWD,
                               'pos.order.line',
                               'search_read',
                               [searchArr],
                               {'fields': [
                                   'name',
                                   'order_id',
                                   'display_name',
                                   'product_id',
                                   'price_unit',
                                   'qty',
                                   'price_subtotal',
                                   'price_subtotal_incl',
                                   'discount',
                                   'create_date'
                               ], 'offset': 0, 'limit': count})

    return [output, count]

# return product category id
async def get_prod_cat(ids=[]):
    if not ids:
        condition = ['id', '>', 0]
    else:
        condition = ['id', 'in', ids]

    output = models.execute_kw(DB, uid, PWD,
                               'product.category',
                               'search_read',
                               [[condition]],
                               {'fields': [
                                   'name',
                                   'complete_name',
                                   'display_name',
                                   'parent_id',
                                   'parent_path',
                                   'child_id',
                                   'product_count',
                                   'create_date',
                               ]})
                               
    output.sort(reverse=False, key=lambda e: e['id'])
    return output


# return product category details by id
# async def get_prod_cat():
#     return models.execute_kw(DB, uid, PWD, 'product.category', 'data', [[['name', '!=', 'a']]])


# async def model_browsing():
#     # client = Client(HOST, DB, USER, PWD)
#     SaleOrder = client['sale.order']
#     s_orders = await SaleOrder.search_records([])
#     for order in s_orders:
#         print(order.name)
#         for line in order.order_line:
#             print("\t%s" % line.name)
#         print("-" * 5)
#         print()


# -----------------
# functions section
# -----------------

# Set Odoo Offset/page to default
async def offset_correction(offset: int):
    if offset > 0:
        offset = offset - 1
    return int(offset)


async def converto(value):
    fmt = valueOf.DATETIME_FORMAT
    tzone = valueOf.TIME_ZONE

    if not value:
        utc = arrow.utcnow()
        to_local = utc.to(tzone.fulltext)
        value = to_local.format(fmt.fulltext)

    toArrow = arrow.get(value)
    local = toArrow.replace(tzinfo=tzone.fulltext)
    START = local.replace(hour=0, minute=0, second=0)
    END = local.replace(hour=23, minute=59, second=59)

    start_to_utc = START.to('UTC').datetime
    end_to_utc = END.to('UTC').datetime

    return [start_to_utc, end_to_utc]


async def massage_date_filter(data, start_from, end_to, count):
    data = await set_dict(data)
    new_list = []
    for i in data:
        date_order = i['date_order']
        if not date_order:
            break

        tzone = valueOf.TIME_ZONE
        fmt = valueOf.DATE_FORMAT
        utc = arrow.get(date_order)
        date_order = utc.to(tzone.fulltext).datetime
        if (date_order <= end_to) and (date_order >= start_from):
            i['date_order'] = utc.datetime
            i['create_date'] = utc.datetime
            [output, total] = await get_pos_order_line(arrow.get(date_order).format(fmt.fulltext), i['id'])
            dict_order = await set_dict(output)
            record = await massage_pos_order_dict(i, dict_order)
            new_list.append(record)
        else:
            count = count - 1

    return [new_list, count]


async def pagination_process(count, size):
    repeat = 0
    if count > size:
        calc = count / size
        if (calc - int(calc)) == 0:
            repeat = int(calc)
        else:
            repeat = int(calc) + 1

        # for i in range(repeat):
        #     print(i)

    return repeat


async def massage_pos_order_dict(data, order_line):
    discount = 0.0
    price_total = 0.0
    price_total_incl_tax = 0.0
    for o in order_line:
        discount = o['discount']
        if discount > 0.0:
            price_total = price_total + (o['price_unit'] * o['qty'])
            # price_total_incl_tax = price_total_incl_tax + \
            #     (price_total - (price_total *
            #      (discount/100)) + data['amount_tax'])
        else:
            price_total = price_total + o['price_subtotal']
            # price_total_incl_tax = price_total_incl_tax + \
            #     o['price_subtotal_incl']

    shop_name = data['config_id'][1]
    altered_name = shop_name.replace(" (not used)", "")
    arr = dict(
        id=data['id'],
        name=data['name'],
        date_order=data['date_order'],
        user_id=data['user_id'],
        shop_name=altered_name,
        price_total=price_total,
        discount_percent=discount,
        amount_tax=data['amount_tax'],
        # price_total_incl_tax=price_total_incl_tax,
        net_amount_total=data['amount_total'],
        amount_paid=data['amount_paid']+data['amount_return'],
        amount_return=data['amount_return'],
        session_id=data['session_id'],
        pos_reference=data['pos_reference'],
        state=data['state'],
        is_invoiced=data['is_invoiced'],
        invoice_ref=data['account_move'],
        is_tipped=data['is_tipped'],
        tip_amount=data['tip_amount'],
        loyalty_points=data['loyalty_points'],
        sale_journal=data['sale_journal'],
        create_date=data['create_date'],
        create_uid=data['create_uid']
    )

    # print(arr)

    return arr
