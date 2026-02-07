from django.contrib import admin
from . import models

@admin.register(models.Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','badge', 'badge_type', 'url', 'order', 'is_active') 
    list_filter = ('is_active',)
    search_fields = ('title',)