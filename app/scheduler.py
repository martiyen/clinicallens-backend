from apscheduler.schedulers.background import BackgroundScheduler
from app.fetch_trials import fetch_and_store_trials
import time

def start_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=fetch_and_store_trials, args=[app], trigger="interval", seconds=10)
    scheduler.start()

# Run 2 schedulers or fetch_and_store_trials twice each interval for some reason. If I save this file, it resets to one. Then, if I restart flask, it is duplicated again.
# Need to investigate /!\