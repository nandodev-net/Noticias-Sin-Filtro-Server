from django.contrib import admin
from app.killswitch.models import KillswithcSettings

# Register your models here.

class KillswitchAdmin(admin.ModelAdmin):
    list_display = ("non_compatible_msg", "upgradable_compatible_msg", "last_version_msg")


admin.site.register(KillswithcSettings, KillswitchAdmin)