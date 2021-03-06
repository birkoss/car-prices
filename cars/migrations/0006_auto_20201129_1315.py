# Generated by Django 3.1.3 on 2020-11-29 18:15

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0005_auto_20201129_0717'),
    ]

    operations = [
        migrations.AddField(
            model_name='trim',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trim',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='trim',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
