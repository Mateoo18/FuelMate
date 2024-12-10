from apscheduler.schedulers.background import BackgroundScheduler
from django.utils.timezone import now
from datetime import timedelta

def start_scheduler():
    from .tasks.ranking_tasks import process_weekly_ranking
    scheduler = BackgroundScheduler()
    # Ustaw harmonogram na poniedziałek o godzinie 00:00
    scheduler.add_job(
        process_weekly_ranking,
        'cron',
        day_of_week='mon',
        hour=0,
        minute=0
    )
    scheduler.start()
