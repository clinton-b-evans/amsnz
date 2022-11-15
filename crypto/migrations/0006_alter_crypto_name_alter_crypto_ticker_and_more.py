# Generated by Django 4.1.1 on 2022-11-15 15:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("crypto", "0005_crypto_user_cryptotransaction_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="crypto",
            name="name",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="crypto",
            name="ticker",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterUniqueTogether(
            name="crypto",
            unique_together={("user", "ticker", "name")},
        ),
    ]
