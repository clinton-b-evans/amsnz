# Generated by Django 4.1.1 on 2022-12-13 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("commodities", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CommodityClass",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("Gold", "Gold"),
                            ("Silver", "Silver"),
                            ("Platinum", "Platinum"),
                            ("Palladium", "Palladium"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "commodity_class",
                    models.CharField(
                        choices=[
                            ("GC=F", "GC=F"),
                            ("SI=F", "SI=F"),
                            ("PL=F", "PL=F"),
                            ("PA=F", "PA=F"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AlterUniqueTogether(
            name="commodity",
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name="commodity",
            name="commodity_class",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="commodities.commodityclass",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="commodity",
            unique_together={("user", "commodity_class", "year")},
        ),
        migrations.RemoveField(
            model_name="commodity",
            name="name",
        ),
    ]
