# Generated by Django 4.0.1 on 2022-05-10 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0033_property_parking_alter_property_vacancy_rate"),
    ]

    operations = [
        migrations.AddField(
            model_name="property",
            name="deposit",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="property",
            name="interest_rate",
            field=models.DecimalField(
                decimal_places=2, max_digits=5, verbose_name="Interest Rate %"
            ),
        ),
        migrations.AlterField(
            model_name="property",
            name="loan_amount",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="property",
            name="loan_term",
            field=models.PositiveIntegerField(default=30),
        ),
        migrations.AlterField(
            model_name="property",
            name="market_value",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="property",
            name="purchase_price",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
