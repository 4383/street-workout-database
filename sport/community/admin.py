from django.contrib import admin
from community.models import InformationMessage


# Register your models here.
class InformationMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'type')


admin.site.register(InformationMessage, InformationMessageAdmin)