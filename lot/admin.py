from django.contrib import admin
from .models import LOT


class LOTAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid',)

admin.site.register(LOT, LOTAdmin)
