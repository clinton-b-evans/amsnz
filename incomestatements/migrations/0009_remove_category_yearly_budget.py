# Generated by Django 4.1.1 on 2022-11-25 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "incomestatements",
            "0008_category_april_budget_category_august_budget_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="category",
            name="yearly_budget",
        ),
    ]
