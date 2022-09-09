
from django.urls import re_path, include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from tools.views import set_up_database
from django.conf import settings
from django.contrib.auth import logout

from products.views import *
from esoda_katastimata.views import homepage as katastimata_homepage
from mysite.views import homepage as mysite_homepage

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    path('', welcome_page, name='welcome_page'),
    re_path(r'^accounts/',include('account.urls')),
    re_path(r'^αποθήκη/',include('products.urls')),
    re_path(r'^πληρωμές-εισπράξεις/',include('transcations.urls')),
    re_path(r'^συνταγές/',include('recipes.urls')),
    re_path(r'^PoS/',include('PoS.urls')),
    re_path(r'^reports/',include('reports.urls')),
	re_path(r'^katastimata/',include('esoda_katastimata.urls')),
    re_path(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),

    # that url setup the database, comment it after the use
    #url(r'^database/',view=set_up_database),





    re_path(r'^inventory/', include('inventory_manager.urls')),
    
    
    re_path(r'^site/$', mysite_homepage,),
    re_path(r'^katastimata/$', katastimata_homepage,),
    re_path(r'^homepage/$', homepage,),
    re_path(r'^homepage/new_all/last_order/$', add_product_to_order,name='last_one'),
    re_path(r'^homepage/new_all/last_order/(?P<dk>\d+)/$',order_done,),
    re_path(r'^homepage/new_all/last_order/edit/(?P<dk>\d+)/$', done_order_edit_id,),
    re_path(r'^homepage/new_all/last_order/product/edit/(?P<dk>\d+)/$', done_order_product_id,),
    re_path(r'^homepage/new_all/last_order/product/add/(?P<dk>\d+)/$', done_order_add_product,),
    re_path(r'^homepage/new_all/last_order/product/delete/(?P<dk>\d+)/$', done_order_delete_id,),



    re_path(r'^homepage/edit_all/$', edit_all,),
    re_path(r'^homepage/edit_all/orders/$', edit_orders_section,),
    re_path(r'^homepage/edit_all/order/(?P<dk>\d+)/$', edit_order,),
    re_path(r'^homepage/edit_all/order_id/(?P<dk>\d+)/$', edit_order_id,),
    re_path(r'^homepage/edit_all/order_id/delete/(?P<dk>\d+)/$', delete_order_id,),
    re_path(r'^homepage/edit_all/orders/add/(?P<dk>\d+)/$', add_order_id,),



    re_path(r'^homepage/edit_all/products/(?P<dk>\d+)/$',edit_product_id,),
    re_path(r'^homepage/edit_all/products/$', products_edit_section,),
    re_path(r'^homepage/edit_all/products/vendor/(?P<dk>\d+)/$',edit_product_vendor_id),

    re_path(r'^homepage/edit_all/vendors/$', edit_vendor_section,),
    re_path(r'^homepage/edit_all/vendors/(?P<dk>\d+)/$', edit_vendor_id,),


    re_path(r'^inventory_informations/$', informations_inventory,),
    re_path(r'^inventory_informations/προμηθευτές/$', info_vendors_section,),
    re_path(r'^inventory_informations/προμηθευτές-ανάλυση/$', info_vendor_personal_stuff,),
    re_path(r'^inventory_informations/προμηθευτές-υπόλοιπο/$', info_vendor_ipoloipo,),
    re_path(r'^inventory_informations/προμηθευτές-υπόλοιπο/(?P<dk>\d+)/$', info_vendor_ipoloipo_id,),
    re_path(r'^inventory_informations/προμηθευτές-ανά-προμηθευτή/$', info_vendor_order,),
    re_path(r'^inventory_informations/προμηθευτές-ανά-προμηθευτή/(?P<dk>\d+)/$', info_vendor_order_id,),




    re_path(r'^inventory_informations/calendar/$', inventory_info_calendar,),
    re_path(r'^inventory_informations/order/$', info_order,),
    re_path(r'^inventory_informations/πληρωμές/$', info_calendar_payments,),


    re_path(r'^inventory_informations/προιόντα/$', info_products,),



    re_path(r'^inventory_informations/κατηγορία/', info_products_category,),
    re_path(r'^inventory_informations/προμηθευτής/', info_products_vendors,),
    re_path(r'^inventory_informations/χονδρική/', info_products_xondriki,),
    re_path(r'^inventory_informations/προιόντα/(?P<dk>\d+)$', info_products_id,),







 




] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


