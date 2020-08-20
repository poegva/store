# Generated by Django 3.1 on 2020-08-19 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20200819_1759'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='shop_quantity',
            field=models.IntegerField(blank=True, default=0, verbose_name='Количество на складе'),
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='items', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='order',
            name='token',
            field=models.CharField(blank=True, default='NO_TOKEN', max_length=32, verbose_name='Токен доступа к заказу'),
        ),
    ]
