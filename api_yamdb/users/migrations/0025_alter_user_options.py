# Generated by Django 3.2 on 2023-04-07 21:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_user_is_superuser'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Пользователь'},
        ),
    ]
