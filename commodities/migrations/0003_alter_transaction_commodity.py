# Generated by Django 4.1.1 on 2022-12-13 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("commodities", "0002_commodityclass_alter_commodity_unique_together_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="commodity",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="commodities.commodityclass",
            ),
        ),
    ]
