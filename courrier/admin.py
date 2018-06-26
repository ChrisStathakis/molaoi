from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
# Register your models here.

@admin.register(Status)
class StatusAdmin(ImportExportModelAdmin):
	list_display = ['title', 'id']


@admin.register(PaymentMethod)
class PaymentMethodAdmin(ImportExportModelAdmin):
	list_display = ['title', 'id']

@admin.register(Shipping)
class ShippingAdmin(ImportExportModelAdmin):
	list_display = ['title', 'id']

@admin.register(WebOrder)
class WebOrderAdmin(ImportExportModelAdmin):
	# radio_fields = {"status": admin.VERTICAL}
	search_fields = ['id', 'name', 'status__title', 'payment_method__title']
	list_display = ['id','date', 'web_order', 'status',
					'payment_method', 	
					'is_paid', 'value', 
					'is_cancel','shipping_cost'
					]
	list_filter = ['is_paid', 'is_cancel', 'date','payment_method', 
				   'shipping_method', 'status']
	