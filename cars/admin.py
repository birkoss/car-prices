from django.contrib import admin

from .models import Make, Model, Trim

admin.site.register(Make)
admin.site.register(Model)
admin.site.register(Trim)
