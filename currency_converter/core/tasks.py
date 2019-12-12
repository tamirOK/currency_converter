from currency_converter import celery_app

from .models import Conversion


@celery_app.task
def update_currency_rates():
    Conversion.update_currency_rates()
