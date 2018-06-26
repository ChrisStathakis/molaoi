from django.contrib import admin
from .models import*
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','description','product_id','category','supplier','price_buy','ekptosi','price_with_discount',]
    list_filter = ['status','supplier','category','carousel']
    fieldsets = (
        ('Στοιχεία',{
            'fields':('title',('description','product_id'),'image',('category','supplier','qty_kilo'),('notes'))
        }),
        ('Οικονομικά Στοιχεία',{
            'classes':('collapse',),
            'fields':(('price_buy','ekptosi'),('reserve','status','safe_stock'),'price')
        }),
        ('Χονδρική',{
            'classes':('collapse',),
            'fields':(('carousel','price_internet'),)
        }),
    )

class SupplyAdmin(admin.ModelAdmin):
    list_display = ['title','phone','phone1','fax','email','site','doy','afm',]
    list_filter = ['doy',]
    fieldsets = (
        ('Στοιχεία',{
            'fields':('title',('phone','phone1','fax'),('email','site'),'address','description')
        }),
        ('Οικονομικά Στοιχεία',{
            'classes':('collapse',),
            'fields':(('doy','afm'),'balance', 'remaining_deposit')
        }),

    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Supply, SupplyAdmin)
admin.site.register(Costumers)
admin.site.register(TaxesCity)


admin.site.register(Color)
admin.site.register(ColorAttribute)

admin.site.register(Size)
admin.site.register(SizeAttribute)




