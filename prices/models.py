from django.db import models

from core.helpers import jsonfield_default_value, slugify_model
from core.models import TimeStampedModel, UUIDModel


class Price(TimeStampedModel, UUIDModel, models.Model):
    trim = models.ForeignKey(
        'cars.Trim',
        on_delete=models.PROTECT,
        null=True
    )

    msrp = models.FloatField()
    delivery = models.FloatField()
    taxes = models.FloatField()

    data = models.JSONField(default=jsonfield_default_value)
    hash = models.CharField(max_length=32, default='')

    is_active = models.BooleanField(default=False)
    is_pending = models.BooleanField(default=False)

    def __str__(self):
        return self.trim.__str__()
