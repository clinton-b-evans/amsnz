# Generated by Django 4.1.1 on 2022-10-13 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0037_alter_property_loan_amount_alter_property_loan_term"),
    ]

    operations = [
        migrations.AlterField(
            model_name="property",
            name="loan_amount",
            field=models.PositiveIntegerField(default=0),
        ),
    ]