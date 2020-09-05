# Generated by Django 3.1 on 2020-09-05 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0004_auto_20200903_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='status',
            field=models.CharField(choices=[('REQUESTED', 'Запрошена'), ('DRAFT', 'Черновик'), ('SUBMITED', 'Оформлена'), ('APPROVED', 'Подтверждена'), ('IN_FULFILLMENT', 'Передана в фулфиллмент'), ('IN_DELIVERY', 'В доставке у провайдера'), ('COMPLETED', 'Выполнена'), ('ERROR', 'Ошибка'), ('CANCELED', 'Отменена')], db_index=True, default='REQUESTED', max_length=25, verbose_name='Статус доставки'),
        ),
    ]
