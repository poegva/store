# Generated by Django 3.1 on 2020-08-19 20:53

from django.db import migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20200819_2043'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'get_latest_by': 'modified'},
        ),
        migrations.AddField(
            model_name='order',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
        ),
    ]