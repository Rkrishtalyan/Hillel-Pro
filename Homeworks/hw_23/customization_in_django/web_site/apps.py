from django.apps import AppConfig


class WebSiteConfig(AppConfig):
    name = 'web_site'

    def ready(self):
        import web_site.signals
