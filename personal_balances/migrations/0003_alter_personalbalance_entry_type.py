# Generated by Django 4.0.1 on 2022-07-26 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal_balances', '0002_alter_personalbalance_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalbalance',
            name='entry_type',
            field=models.CharField(choices=[('Asset', 'Asset'), ('Liability', 'Liability'), ('Savings', 'Savings'), ('Retirement Acc', 'Retirement Acc')], max_length=100),
        ),
    ]
