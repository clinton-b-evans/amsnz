# Generated by Django 4.0.1 on 2022-05-24 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal_balances', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalbalance',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
