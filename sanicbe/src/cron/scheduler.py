import datetime as dt

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from views.odoo import get_export_order
from models.role import Role
from sqlalchemy import select


async def odooWarehouse(bar, app):
    print('Cronjob running at: %s - %s' % (dt.datetime.now(), bar))
    async with app.db.connect() as conn:
        stmt = select(Role).where(Role.name == 'Admin')
        data = await conn.execute(stmt)
        print("successss", data.scalar())

    # await get_export_order()


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
