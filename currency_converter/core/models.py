from django.conf import settings
from django.db import models
from django.utils import timezone
from decimal import Decimal

import logging

import requests

logger = logging.getLogger(__name__)


class Conversion(models.Model):

    RATES_EXCHANGE_URL = 'https://openexchangerates.org/api/latest.json'

    SUPPORTED_CURRENCIES = (
        ('CZK', 'Koruna'),
        ('EUR', 'Euro'),
        ('PLN', 'Zloty'),
        ('USD', 'US Dollar'),
    )

    source_currency = models.CharField(max_length=3, choices=SUPPORTED_CURRENCIES)
    destination_currency = models.CharField(max_length=3, choices=SUPPORTED_CURRENCIES)
    rate = models.DecimalField(max_digits=20, decimal_places=10)
    updated_at = models.DateTimeField(default=timezone.now())

    @classmethod
    def _update_currency_rates(cls, data):
        rates = data["rates"]
        currency_pairs = [
            (source, dest)
            for source in rates.keys()
            for dest in rates.keys()
            if source != dest
        ]
        update_dt = timezone.now()
        insert_data = [
            Conversion(
                source_currency=source,
                destination_currency=destination,
                rate=Decimal(rates[destination]) / Decimal(rates[source]),
                updated_at=update_dt
            )
            for source, destination in currency_pairs
        ]

        cls.objects.bulk_create(insert_data)

    @classmethod
    def update_currency_rates(cls):
        try:
            symbols = ','.join(code for code,_  in cls.SUPPORTED_CURRENCIES)
            params = {
                'app_id': settings.APP_ID,
                'symbols': symbols
            }
            data = requests.get(cls.RATES_EXCHANGE_URL, params=params).json()
            return cls._update_currency_rates(data)
        except requests.exceptions.BaseHTTPError as exc:
            logger.exception(str(exc))
