# Generated by Django 4.0.1 on 2022-06-09 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CashFlow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('entry_type', models.CharField(choices=[('Income', 'Income'), ('Expense', 'Expense')], max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
    ]
