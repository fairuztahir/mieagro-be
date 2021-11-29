import datetime as dt

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from views.warehouse import migrateWarehouseToDB
from helpers.func import valueOf


async def odoo(job, app):
    print('Cronjob running at: %s - %s' % (dt.datetime.now(), job))
    app.add_task(migrateWarehouseToDB(app))


def assign_time(year="*", month="*", day="*", hour="*", minute="*", second="*"):
    trigger = CronTrigger(
        year=year, month=month, day=day, hour=hour, minute=minute, second=second
    )
    return trigger


scheduler = AsyncIOScheduler(timezone=valueOf.UTC_ZONE.fulltext)


async def main(app, loop):
    # Example to run by time gap
    scheduler.add_job(odoo, 'interval', minutes=2, args=["Odoo", app])

    # Run cron with specific time in UTC
    # scheduler.add_job(odoo, trigger=assign_time("*", "*", "*", "11",
    #                                             "30", "0"), args=["Odoo"], name="daily Odoo")
    # or
    # scheduler.add_job(odoo, "cron", day_of_week="mon-fri", hour = "16")

    scheduler.start()


async def stop():
    scheduler.shutdown(False)
