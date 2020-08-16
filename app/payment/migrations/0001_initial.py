# Generated by Django 3.1 on 2020-08-15 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0005_order_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yandex_id', models.CharField(max_length=200, verbose_name='ID в Яндекс Кассе')),
                ('status', models.CharField(db_index=True, max_length=20, verbose_name='Статус платежа')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма платежа')),
                ('currency', models.CharField(default='RUB', max_length=3, verbose_name='Валюта платежа')),
                ('confirmation_token', models.CharField(max_length=200, null=True, verbose_name='Токен подтверждения')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.order', verbose_name='Заказ')),
            ],
        ),
    ]