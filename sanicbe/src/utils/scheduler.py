import datetime as dt
import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from views.warehouse import migrateWarehouseToDB
from views.product import migrateProductToDB
from views.attribute import migrateAttributeToDB
from views.attribute_value import migrateAttributeValueToDB
from views.product_attribute_line import migrateProdAttributeLineToDB
from views.product_attribute_value import migrateProdAttributeValueToDB
from views.product_variant import migrateProdVariantToDB
from views.product_category import migrateProdCategoryToDB
from helpers.func import valueOf


async def odoo(job, app):
    print('Cronjob running at: %s - %s' % (dt.datetime.now(), job))
    app.add_task(migrateWarehouseToDB(app))
    await asyncio.sleep(5)
    app.add_task(migrateProdCategoryToDB(app))
    await asyncio.sleep(5)
    app.add_task(migrateProductToDB(app))
    await asyncio.sleep(5)
    app.add_task(migrateAttributeToDB(app))
    await asyncio.sleep(5)
    app.add_task(migrateAttributeValueToDB(app))
    await asyncio.sleep(5)
    app.add_task(migrateProdAttributeLineToDB(app))
    await asyncio.sleep(5)
    app.add_task(migrateProdAttributeValueToDB(app))
    await asyncio.sleep(5)
    app.add_task(migrateProdVariantToDB(app))


def assign_time(year="*", month="*", day="*", hour="*", minute="*", second="*"):
    trigger = CronTrigger(
        year=year, month=month, day=day, hour=hour, minute=minute, second=second
    )
    return trigger


scheduler = AsyncIOScheduler(timezone=valueOf.UTC_ZONE.fulltext)


async def main(app, loop):
    # Example to run by time gap
    scheduler.add_job(odoo, 'interval', hours=3, minutes=2, args=["Odoo", app])

    # Run cron with specific time in UTC
    # scheduler.add_job(odoo, trigger=assign_time("*", "*", "*", "11",
    #                                             "30", "0"), args=["Odoo"], name="daily Odoo")
    # or
    # scheduler.add_job(odoo, "cron", day_of_week="mon-fri", hour = "16")

    scheduler.start()


async def stop():
    scheduler.shutdown(False)
