from django.apps import AppConfig
from django.urls import include
from django.urls import path


class CoreAppConfig(AppConfig):
    name = 'front'
    verbose_name = 'Front app config'

    def ready(self):
        super().ready()
        from private_library.urls import urlpatterns
        urlpatterns.append(path('', include('front.urls')),)
