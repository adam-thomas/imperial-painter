from django.contrib import admin

from . import models


class FilePathAdmin(admin.ModelAdmin):
    list_display = ["__str__", "generator_key"]


admin.site.register(models.Card, admin.ModelAdmin)
admin.site.register(models.CachedFilePath, FilePathAdmin)
