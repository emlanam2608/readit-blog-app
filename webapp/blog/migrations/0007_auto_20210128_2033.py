# Generated by Django 2.2.17 on 2021-01-28 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20210128_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='flag',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]
