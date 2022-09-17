from django.apps import AppConfig


class NewsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsapp'


class PostConfig(AppConfig):
    name = 'newsapp'

    def ready(self):
        import newsapp.signals
