from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_filter = ['is_readed']
    list_display = ['subject', 'last_name', 'first_name', 'date_created', 'is_readed']
    ordering = ['date_created', 'last_name']



admin.site.register(NewsLetterUser, ImportExportModelAdmin)
admin.site.register(NewsLetterEmail, ImportExportModelAdmin)
admin.site.register(Contact, ContactAdmin)
