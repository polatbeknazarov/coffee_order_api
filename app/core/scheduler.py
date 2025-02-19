from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.clear_unverified_users import remove_unverified_users

scheduler = AsyncIOScheduler()
scheduler.add_job(remove_unverified_users, "interval", days=2)
