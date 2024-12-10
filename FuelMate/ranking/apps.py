from django.apps import AppConfig
class RankingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ranking'

    def ready(self):
        from .scheduler import start_scheduler
        start_scheduler()
