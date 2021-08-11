from django.contrib import admin
from .models import TrickSet, Combo


class TrickSetAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')


class ComboAdmin(admin.ModelAdmin):
    list_display = ('author', 'combo_name')


admin.site.register(Combo, ComboAdmin)
admin.site.register(TrickSet, TrickSetAdmin)
