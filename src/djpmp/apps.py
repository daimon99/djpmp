from django.apps import AppConfig


class DjpmpConfig(AppConfig):
    name = 'djpmp'
    verbose_name = 'djpmp'

    def ready(self):
        from .signals import handlers
        handlers  # 避免被 pycharm 优化掉
