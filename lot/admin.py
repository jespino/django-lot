from django.contrib import admin
from .models import LOT


class LOTAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'user', 'type', 'created',)
    list_filter = ('type',)
    readonly_fields = ('uuid',)

admin.site.register(LOT, LOTAdmin)
