from django.forms import ModelForm, DecimalField

from .models import Conversion


class ConversionForm(ModelForm):

    amount = DecimalField(min_value=0)

    class Meta:
        model = Conversion
        exclude = ['id', 'rate', 'updated_at']
        supported_currencies = [short for short, _ in Conversion.SUPPORTED_CURRENCIES]
        wrong_currency_msg = 'Supported currencies are: %s' % (', '.join(supported_currencies))
        error_messages = {
            'source_currency': {
                'invalid_choice': wrong_currency_msg
            },
            'destination_currency': {
                'invalid_choice': wrong_currency_msg
            }
        }
