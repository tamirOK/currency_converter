from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Conversion
import responses


class TestConversionModel(TestCase):
    @responses.activate
    def test_update_currency_rates(self):
        """
            Checks fetching currency rates and inserting them into DB
        """
        return_data = {
            'disclaimer': 'Usage subject to terms: https://openexchangerates.org/terms',
            'license': 'https://openexchangerates.org/license',
            'timestamp': 1575838753,
            'base': 'USD',
            'rates': {'CZK': 23.10615, 'EUR': 0.904319, 'PLN': 3.8695, 'USD': 1}
        }
        responses.add(responses.GET, Conversion.RATES_EXCHANGE_URL, json=return_data)
        Conversion.update_currency_rates()
        # check inserted data count
        self.assertEqual(Conversion.objects.count(), 12)
        # check inserted data
        currencies = ('CZK', 'EUR', 'PLN', 'USD')
        for source in currencies:
            for dest in currencies:
                if source != dest:
                    self.assertEqual(
                        Conversion.objects.filter(source_currency=source, destination_currency=dest).count(),
                        1,
                        "Every pair of currencies must be inserted only once"
                    )


class TestShowRatesView(TestCase):

    def setUp(self):
        currencies = ('CZK', 'EUR', 'PLN', 'USD')
        rates = {
            'EUR': {
                'CZK': Decimal(2),
                'PLN': Decimal(3),
                'USD': Decimal(4),
            },
            'CZK': {
                'EUR': Decimal(1 / 2),
                'PLN': Decimal(5),
                'USD': Decimal(6),
            },
            'PLN': {
                'CZK': Decimal(1/ 5),
                'EUR': Decimal(1 / 3),
                'USD': Decimal(7),
            },
            'USD': {
                'CZK': Decimal(1 / 6),
                'PLN': Decimal(1 / 7),
                'EUR': Decimal(1 / 4),
            }
        }
        insert_data = []
        for source in currencies:
            for dest in currencies:
                if source != dest:
                    insert_data.append(
                        Conversion(source_currency=source, destination_currency=dest, rate=rates[source][dest])
                    )
        Conversion.objects.bulk_create(insert_data)

    def test_show_all_rates(self):
        response = self.client.get(reverse("rates"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 12)


class TestConvertView(TestCase):
    def setUp(self):
        Conversion.objects.create(source_currency="USD", destination_currency="EUR", rate=Decimal("0.93"))

    def test_convert_api(self):
        params = {
            "source_currency": "USD",
            "destination_currency": "EUR",
            "amount": 731
        }
        response = self.client.get(reverse("convert"), params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "ok")
        self.assertEqual(response.data["result"]["converted"], 731 * Decimal("0.93"))

    def test_convert_api_invalid_data(self):
        params = {
            "source_currency": "ABC",
            "destination_currency": "EUR",
            "amount": -1
        }
        response = self.client.get(reverse("convert"), params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "error")
        self.assertEqual(response.data["result"]["source_currency"], ['Supported currencies are: CZK, EUR, PLN, USD'])
        self.assertEqual(response.data["result"]["amount"], ['Ensure this value is greater than or equal to 0.'])
