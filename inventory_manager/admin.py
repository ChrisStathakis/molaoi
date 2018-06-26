from django.contrib import admin
from .models import *
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['code','vendor','date','total_price',]
    list_filter=['vendor','date']

admin.site.register(Unit)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(PayOrders)
admin.site.register(PaymentMethod)
admin.site.register(PaymentMethodGroup)