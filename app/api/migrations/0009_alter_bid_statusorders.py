# Generated by Django 4.1.3 on 2022-12-27 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_bid_statusordernotification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='statusOrders',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
