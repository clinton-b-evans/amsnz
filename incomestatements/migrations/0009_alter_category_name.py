# Generated by Django 4.1.1 on 2023-01-26 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("incomestatements", "0008_alter_incomestatement_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(max_length=120),
        ),
    ]