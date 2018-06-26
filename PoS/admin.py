from django.contrib import admin
from .models import *

# Register your models here.

class TableAdmin(admin.ModelAdmin):
    list_display =['title','status']
    
    class Meta:
        model = Table



admin.site.register(Table, TableAdmin)
admin.site.register(RestoOrder)
admin.site.register(DailyIncomeGreG)
admin.site.register(MonthlyIncomeGreG)
admin.site.register(YearlyIncomeGreg)
admin.site.register(Lianiki_Order)
