# Generated by Django 4.2.7 on 2023-12-09 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental_api', '0022_delete_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='iha',
            name='is_active',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]