# Generated by Django 3.1.3 on 2020-11-30 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prices', '0007_auto_20201129_1904'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='is_pending',
            field=models.BooleanField(default=False),
        ),
    ]
