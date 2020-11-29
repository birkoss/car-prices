from django.contrib import admin

from prices.models import Price, PriceType


admin.site.register(Price)
admin.site.register(PriceType)
