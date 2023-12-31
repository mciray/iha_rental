# Generated by Django 4.2.7 on 2023-12-04 05:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rental_api', '0013_alter_rental_car_alter_rental_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Iha',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('make', models.CharField(max_length=100)),
                ('weight', models.IntegerField()),
                ('model', models.CharField(max_length=100)),
                ('year', models.PositiveIntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('price_per_day', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='wallet',
            name='user',
        ),
        migrations.RemoveField(
            model_name='rental',
            name='car',
        ),
        migrations.RenameModel(
            old_name='Cartype',
            new_name='Ihatype',
        ),
        migrations.DeleteModel(
            name='Car',
        ),
        migrations.DeleteModel(
            name='Wallet',
        ),
        migrations.AddField(
            model_name='iha',
            name='iha_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rental_api.ihatype'),
        ),
        migrations.AddField(
            model_name='rental',
            name='iha',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rental_api.iha'),
        ),
    ]
