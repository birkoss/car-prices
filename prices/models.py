from django.db import models

from core.helpers import jsonfield_default_value, slugify_model
from core.models import TimeStampedModel, UUIDModel


class Price(TimeStampedModel, UUIDModel, models.Model):
    type = models.ForeignKey(
        'PriceType',
        on_delete=models.PROTECT,
        null=True
    )

    data = models.JSONField(default=jsonfield_default_value)


class PriceType(TimeStampedModel, UUIDModel, models.Model):
    name = models.CharField(max_length=100, default='')
    slug = models.SlugField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug.strip():
            self.slug = slugify_model(PriceType, self.__str__())
        super(PriceType, self).save()
