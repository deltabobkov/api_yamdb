# Generated by Django 3.2 on 2023-03-29 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20230329_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'admin'), (2, 'user'), (3, 'moderator')], null=True),
        ),
    ]
