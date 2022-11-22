# Generated by Django 4.1.1 on 2022-11-18 13:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("properties", "0038_alter_property_loan_amount"),
    ]

    operations = [
        migrations.AddField(
            model_name="property",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="property",
            name="property_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Residential", "Residential"),
                    ("Commercial", "Commercial"),
                    ("Industrial", "Industrial"),
                    ("Retail", "Retail"),
                    ("Land", "Land"),
                    ("Other", "Other"),
                ],
                max_length=100,
                null=True,
            ),
        ),
    ]
