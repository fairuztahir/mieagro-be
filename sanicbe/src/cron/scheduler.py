import datetime as dt

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from views.warehouse import migrateWarehouseToDB


async def odooWarehouse(bar, app):
    print('Cronjob running at: %s - %s' % (dt.datetime.now(), bar))
    app.add_task(migrateWarehouseToDB(app))


def assign_time(year="*", month="*", day="*", hour="*", minute="*", second="*"):
    trigger = CronTrigger(
        year=year, month=month, day=day, hour=hour, minute=minute, second=second
    )
    return trigger


scheduler = AsyncIOScheduler()


async def main(app, loop):
    # Example to run by time gap
    scheduler.add_job(odooWarehouse, 'interval', minutes=1, args=["Odoo", app])

    # Run cron with specific time in UTC
    # scheduler.add_job(odoo, trigger=assign_time("*", "*", "*", "11",
    #                                             "30", "0"), args=["Odoo"], name="daily Odoo")

    scheduler.start()


async def stop():
    scheduler.shutdown(False)
