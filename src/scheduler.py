import schedule
import time
from src.etl_pipeline import run_etl
from src.config import DEFAULT_CITIES

def start_scheduler():
    schedule.every(60).minutes.do(lambda: run_etl(DEFAULT_CITIES))

    print("✅ Scheduler started. Running every 60 minutes...")

    while True:
        schedule.run_pending()
        time.sleep(1)
