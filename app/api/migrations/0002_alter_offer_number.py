# Generated by Django 4.1.3 on 2022-12-14 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='number',
            field=models.BigIntegerField(primary_key=True, serialize=False, unique=True, verbose_name='Номер заявки на продажу'),
        ),
    ]
