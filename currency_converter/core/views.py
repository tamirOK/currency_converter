import logging
from decimal import Decimal

from django.db import connection
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import ConversionForm
from .models import Conversion
from .serializers import ConversionSerializer

logger = logging.getLogger(__name__)


class ShowRates(ListAPIView):
    serializer_class = ConversionSerializer
    queryset = Conversion.objects.all()


class ConvertView(APIView):

    def get(self, request):
        form = ConversionForm(request.query_params)
        if not form.is_valid():
            return Response({
                "status": "error",
                "result": form.errors
            })
        else:
            try:
                # Generate such query via Django ORM is cumbersome
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT rate
                        FROM core_conversion
                        WHERE source_currency = %s AND destination_currency = %s AND
                              updated_at = (
                                SELECT MAX(updated_at) FROM core_conversion
                              );
                """, [form.cleaned_data["source_currency"], form.cleaned_data["destination_currency"]])
                    rate = cursor.fetchone()[0]
                return Response({
                    "status": "ok",
                    "result": {
                        "source_currency": form.cleaned_data["source_currency"],
                        "destination_currency": form.cleaned_data["destination_currency"],
                        "amount": form.cleaned_data["amount"],
                        "converted": form.cleaned_data["amount"] * Decimal(rate)
                    }
                })
            except Exception as exc:
                logger.exception(str(exc))
