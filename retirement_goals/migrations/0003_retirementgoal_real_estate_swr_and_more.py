# Generated by Django 4.0.1 on 2022-07-07 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("retirement_goals", "0002_rename_collections_retirementgoal_collectables"),
    ]

    operations = [
        migrations.AddField(
            model_name="retirementgoal",
            name="real_estate_swr",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=4, verbose_name="RE SWR"
            ),
        ),
        migrations.AddField(
            model_name="retirementgoal",
            name="stocks_swr",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=4, verbose_name="Stocks SWR"
            ),
        ),
    ]
