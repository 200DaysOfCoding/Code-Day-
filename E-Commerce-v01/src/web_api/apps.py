from django.apps import AppConfig


class WebApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web_api'

    def ready(self):
        import web_api.signals
