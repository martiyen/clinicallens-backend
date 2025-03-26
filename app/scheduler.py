from apscheduler.schedulers.background import BackgroundScheduler
from app.fetch_trials import fetch_and_store_trials

def start_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=fetch_and_store_trials, args=[app], trigger="interval", hours=24)
    scheduler.start()