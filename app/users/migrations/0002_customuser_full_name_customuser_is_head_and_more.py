# Generated by Django 4.1.3 on 2022-12-10 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='full_name',
            field=models.CharField(max_length=255, null=True, verbose_name='ФИО'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_head',
            field=models.BooleanField(default=False, verbose_name='Руководитель'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='registration_number',
            field=models.IntegerField(max_length=20, null=True, verbose_name='Регистрационный номер'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=100, verbose_name='Пароль'),
        ),
    ]
