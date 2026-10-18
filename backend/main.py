from apscheduler.schedulers.blocking import BlockingScheduler
from backend.scrapper import scrap
from zoneinfo import ZoneInfo

def main():
    # Set up schedular to run the scrapping process every day at 1AM
    scheduler: BlockingScheduler = BlockingScheduler(timezone=ZoneInfo("Australia/Sydney"))
    scheduler.add_job(scrap, "cron", day = "*", hour = "1", minute="0")

    print("Scheduler ready")
    scheduler.start()

if __name__ == "__main__":
    main()
