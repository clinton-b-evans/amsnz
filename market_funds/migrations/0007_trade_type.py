# Generated by Django 4.0.1 on 2022-05-31 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market_funds', '0006_trade_indexfund'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='type',
            field=models.CharField(choices=[('Buy', 'Buy'), ('Sell', 'Sell')], max_length=100, null=True),
        ),
    ]
