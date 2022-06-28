from django.contrib.gis import admin

from . import models


@admin.register(models.Creature)
class CreatureAdmin(admin.ModelAdmin):
    search_fields = ['vendor_id', 'id', 'name']
    list_filter = ['created_at', 'updated_at']
