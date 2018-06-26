
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from tools.views import set_up_database
from django.conf import settings
from django.contrib.auth.views import logout

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$','products.views.welcome_page',name='welcome_page'),
    url(r'^accounts/',include('account.urls')),
    url(r'^αποθήκη/',include('products.urls')),
    url(r'^πληρωμές-εισπράξεις/',include('transcations.urls')),
    url(r'^συνταγές/',include('recipes.urls')),
    url(r'^PoS/',include('PoS.urls')),
    url(r'^reports/',include('reports.urls')),
	url(r'^katastimata/',include('esoda_katastimata.urls')),
    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),

    # that url setup the database, comment it after the use
    #url(r'^database/',view=set_up_database),





    url(r'^inventory/',include('inventory_manager.urls')),
    
    
    url(r'^site/$','mysite.views.homepage',),
    url(r'^katastimata/$','esoda_katastimata.views.homepage',),
    url(r'^homepage/$','products.views.homepage',),
    url(r'^homepage/new_all/last_order/$','products.views.add_product_to_order',name='last_one'),
    url(r'^homepage/new_all/last_order/(?P<dk>\d+)/$','products.views.order_done',),
    url(r'^homepage/new_all/last_order/edit/(?P<dk>\d+)/$','products.views.done_order_edit_id',),
    url(r'^homepage/new_all/last_order/product/edit/(?P<dk>\d+)/$','products.views.done_order_product_id',),
    url(r'^homepage/new_all/last_order/product/add/(?P<dk>\d+)/$','products.views.done_order_add_product',),
    url(r'^homepage/new_all/last_order/product/delete/(?P<dk>\d+)/$','products.views.done_order_delete_id',),



    url(r'^homepage/edit_all/$','products.views.edit_all',),
    url(r'^homepage/edit_all/orders/$','products.views.edit_orders_section',),
    url(r'^homepage/edit_all/order/(?P<dk>\d+)/$','products.views.edit_order',),
    url(r'^homepage/edit_all/order_id/(?P<dk>\d+)/$','products.views.edit_order_id',),
    url(r'^homepage/edit_all/order_id/delete/(?P<dk>\d+)/$','products.views.delete_order_id',),
    url(r'^homepage/edit_all/orders/add/(?P<dk>\d+)/$','products.views.add_order_id',),



    url(r'^homepage/edit_all/products/(?P<dk>\d+)/$','products.views.edit_product_id',),
    url(r'^homepage/edit_all/products/$','products.views.products_edit_section',),
    url(r'^homepage/edit_all/products/vendor/(?P<dk>\d+)/$','products.views.edit_product_vendor_id'),

    url(r'^homepage/edit_all/vendors/$','products.views.edit_vendor_section',),
    url(r'^homepage/edit_all/vendors/(?P<dk>\d+)/$','products.views.edit_vendor_id',),


    url(r'^inventory_informations/$','products.views.informations_inventory',),
    url(r'^inventory_informations/προμηθευτές/$','products.views.info_vendors_section',),
    url(r'^inventory_informations/προμηθευτές-ανάλυση/$','products.views.info_vendor_personal_stuff',),
    url(r'^inventory_informations/προμηθευτές-υπόλοιπο/$','products.views.info_vendor_ipoloipo',),
    url(r'^inventory_informations/προμηθευτές-υπόλοιπο/(?P<dk>\d+)/$','products.views.info_vendor_ipoloipo_id',),
    url(r'^inventory_informations/προμηθευτές-ανά-προμηθευτή/$','products.views.info_vendor_order',),
    url(r'^inventory_informations/προμηθευτές-ανά-προμηθευτή/(?P<dk>\d+)/$','products.views.info_vendor_order_id',),




    url(r'^inventory_informations/calendar/$','products.views.inventory_info_calendar',),
    url(r'^inventory_informations/order/$','products.views.info_order',),
    url(r'^inventory_informations/πληρωμές/$','products.views.info_calendar_payments',),


    url(r'^inventory_informations/προιόντα/$','products.views.info_products',),



    url(r'^inventory_informations/κατηγορία/','products.views.info_products_category',),
    url(r'^inventory_informations/προμηθευτής/','products.views.info_products_vendors',),
    url(r'^inventory_informations/χονδρική/','products.views.info_products_xondriki',),
    url(r'^inventory_informations/προιόντα/(?P<dk>\d+)$','products.views.info_products_id',),












] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


