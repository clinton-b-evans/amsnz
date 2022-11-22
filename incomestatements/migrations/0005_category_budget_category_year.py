# Generated by Django 4.1.1 on 2022-11-22 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("incomestatements", "0004_alter_incomestatement_category_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="budget",
            field=models.DecimalField(
                blank=True, decimal_places=2, default=0.0, max_digits=12
            ),
        ),
        migrations.AddField(
            model_name="category",
            name="year",
            field=models.CharField(default=1, max_length=4),
            preserve_default=False,
        ),
    ]
