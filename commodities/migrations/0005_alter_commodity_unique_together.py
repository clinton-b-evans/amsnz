# Generated by Django 4.1.1 on 2022-11-15 15:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("commodities", "0004_alter_commodity_commodity_class_alter_commodity_name"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="commodity",
            unique_together={("user", "commodity_class", "name")},
        ),
    ]