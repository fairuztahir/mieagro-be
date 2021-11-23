import csv
import io
import moment

from sanic import response
from sanic import Blueprint
from sanic.views import HTTPMethodView
from odoo.main import set_pos_order
from helpers.helpers import valueOf, exceptionRaise, is_valid_date, resJson, resType
from zoneinfo import ZoneInfo
from datetime import datetime


class DownloadCSVView(HTTPMethodView):
    c = Blueprint('csv', url_prefix='/')

    @c.get("/download")
    async def get(request):
        try:
            date = request.args.get('to_date', None)
            if date:
                [flag, valid_date] = await is_valid_date(date)
                if not flag:
                    return resJson(resType.INVALID_DATE)
                else:
                    date = valid_date

            content_type = 'text/csv'
            [rows, count] = await set_pos_order(date)

            if count == 0:
                rows = [
                    dict(
                        id=None,
                        name=None,
                        date_order=None,
                        user_id=None,
                        shop_name=None,
                        price_total=None,
                        discount_percent=None,
                        amount_tax=None,
                        # price_total_incl_tax=None,
                        net_amount_total=None,
                        amount_paid=None,
                        amount_return=None,
                        session_id=None,
                        pos_reference=None,
                        state=None,
                        is_invoiced=None,
                        invoice_ref=None,
                        is_tipped=None,
                        tip_amount=None,
                        loyalty_points=None,
                        sale_journal=None,
                        create_date=None,
                        create_uid=None
                    )
                ]

            fieldnames = rows[0].keys()

            async def streaming_fn(response):
                data = io.StringIO()
                writer = csv.DictWriter(
                    data,
                    fieldnames=fieldnames,
                    extrasaction='ignore'
                )
                writer.writeheader()
                for row in rows:
                    writer.writerow(row)

                await response.write(data.getvalue())

            tzone = valueOf.TIME_ZONE
            fmt = valueOf.DATE_FORMAT

            file_date = None
            if date:
                file_date = moment.date(date).format(fmt.fulltext)
            else:
                file_date = moment.utcnow().timezone(tzone.fulltext).format(fmt.fulltext)

            return response.stream(
                streaming_fn,
                content_type=content_type,
                headers={
                    'Content-Disposition': 'attachment; filename="pos-order-{}.csv";'.format(file_date),
                    'Content-Type': content_type,
                }
            )

        except:
            exceptionRaise('getDownloadCSV')
