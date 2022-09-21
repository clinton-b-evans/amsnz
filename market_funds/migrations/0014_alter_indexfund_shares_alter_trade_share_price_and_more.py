# Generated by Django 4.0.1 on 2022-06-07 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market_funds', '0013_rename_price_indexfund_share_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indexfund',
            name='shares',
            field=models.DecimalField(blank=True, decimal_places=4, default=0.0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='trade',
            name='share_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='trade',
            name='shares',
            field=models.DecimalField(blank=True, decimal_places=4, default=0.0, max_digits=12),
        ),
    ]
