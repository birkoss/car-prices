# Generated by Django 3.1.3 on 2020-12-02 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prices', '0008_price_is_pending'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='price',
            name='type',
        ),
        migrations.AddField(
            model_name='price',
            name='delivery',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='price',
            name='msrp',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='price',
            name='taxes',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='PriceType',
        ),
    ]
