# Generated by Django 4.0.1 on 2022-01-06 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0005_alter_property_insurance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='insurance',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='maintenance',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='management_fee',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
    ]
