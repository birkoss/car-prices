from django.db import models

from core.helpers import slugify_model
from core.models import TimeStampedModel, UUIDModel


class Make(TimeStampedModel, UUIDModel, models.Model):
    name = models.CharField(max_length=255, default="")
    slug = models.SlugField(blank=True, default="")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug.strip():
            self.slug = slugify_model(Make, self.name)
        super(Make, self).save()
