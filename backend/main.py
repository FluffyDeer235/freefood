from apscheduler import BlockingScheduler
from scrapper import scrap

def main():
    scheduler: BlockingScheduler = BlockingScheduler()
    scheduler.add_job(scrap, "cron", day = "*", hour = "1")

    scheduler.start()

if __name__ == "__main__":
    main()
