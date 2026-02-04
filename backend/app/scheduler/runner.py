import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.logging import configure_logging
from app.db.init_db import init_db
from app.scheduler.jobs import run_crawl_sampler

configure_logging()


def main() -> None:
    # Ensure tables exist in the worker too
    init_db()

    scheduler = BackgroundScheduler(timezone="UTC")

    # MVP: every 15 minutes. For class demos: "*/1 * * * *"
    scheduler.add_job(run_crawl_sampler, CronTrigger.from_crontab("*/15 * * * *"), id="crawl_sampler")

    scheduler.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.shutdown()


if __name__ == "__main__":
    main()