# Generated by Django 4.0.1 on 2022-05-10 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0032_alter_property_bathrooms_alter_property_bedrooms_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='parking',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='property',
            name='vacancy_rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Vacancy Rate %'),
        ),
    ]
