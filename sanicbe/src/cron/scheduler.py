import datetime as dt

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from views.odoo import get_export_order


async def odoo(bar):
    print('Cronjob running at: %s - %s' % (dt.datetime.now(), bar))
    # await get_export_order()


def assign_time(year="*", month="*", day="*", hour="*", minute="*", second="*"):
    trigger = CronTrigger(
        year=year, month=month, day=day, hour=hour, minute=minute, second=second
    )
    return trigger


scheduler = AsyncIOScheduler()


async def main(app, loop):
    # Example to run by time gap
    scheduler.add_job(odoo, 'interval', minutes=15, args=["Odoo"])

    # Run cron with specific time in UTC
    # scheduler.add_job(odoo, trigger=assign_time("*", "*", "*", "11",
    #                                             "30", "0"), args=["Odoo"], name="daily Odoo")

    scheduler.start()


async def stop():
    scheduler.shutdown(False)
