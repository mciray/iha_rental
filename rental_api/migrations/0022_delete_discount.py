# Generated by Django 4.2.7 on 2023-12-09 06:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rental_api', '0021_discount'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Discount',
        ),
    ]