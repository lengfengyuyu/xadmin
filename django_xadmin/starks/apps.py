from django.apps import AppConfig

from django.utils.module_loading import autodiscover_modules
class StarksConfig(AppConfig):
    name = 'starks'
    def ready(self):
        autodiscover_modules('starks')