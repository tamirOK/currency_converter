# Generated by Django 2.2.8 on 2019-12-12 00:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conversion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_currency', models.CharField(choices=[('CZK', 'Koruna'), ('EUR', 'Euro'), ('PLN', 'Zloty'), ('USD', 'US Dollar')], max_length=3)),
                ('destination_currency', models.CharField(choices=[('CZK', 'Koruna'), ('EUR', 'Euro'), ('PLN', 'Zloty'), ('USD', 'US Dollar')], max_length=3)),
                ('rate', models.DecimalField(decimal_places=10, max_digits=20)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2019, 12, 12, 0, 30, 17, 871888, tzinfo=utc))),
            ],
        ),
    ]
