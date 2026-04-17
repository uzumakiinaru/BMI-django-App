from django.apps import AppConfig


class BmiAppConfig(AppConfig):
    name = 'bmi_app'

def ready(self):
    import bmi_app.signals