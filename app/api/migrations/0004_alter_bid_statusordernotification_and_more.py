# Generated by Django 4.1.3 on 2022-12-24 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_offer_status_in_trade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='statusOrderNotification',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='bid',
            name='statusOrders',
            field=models.CharField(default=None, max_length=100),
        ),
    ]