# Generated by Django 4.2.4 on 2023-08-29 03:04

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('countries', '0011_alter_tripplace_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tripplace',
            name='duration',
            field=models.DecimalField(decimal_places=2, max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.1'))]),
        ),
        migrations.AlterField(
            model_name='tripplace',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip_places', to='countries.trip'),
        ),
    ]