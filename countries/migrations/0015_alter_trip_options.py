# Generated by Django 4.2.4 on 2023-08-29 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('countries', '0014_trip_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trip',
            options={'permissions': [('duplicate_trip', 'Can duplicate trip')]},
        ),
    ]
