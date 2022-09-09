from django.urls import re_path
from .views import *

urlpatterns =[
    re_path(r"^/$", homepage, name='inventory'),
    re_path(r"^vendors/$", vendors, name="vendors"),
    re_path(r'vendors/edit/$', vendors_edit, name="edit_vendors"),
    re_path(r'vendors/edit/(?P<dk>\d+)/$', vendors_edit_id, name="edit_vendor_id"),
    re_path(r'vendors/details/$', vendors_details, name="vendor_details"),
    re_path(r'vendors/details/(?P<dk>\d+)/$', vendor_analytics, name="vendor_ana"),

    re_path(r'^products/$', products, name="products"),

    re_path(r'^products/vendor/(?P<dk>\d+)/$', edit_product_vendor, name="edit_products_vendor"),

    re_path(r'^products/edit/$', edit_product, name="edit_product"),
    re_path(r'^products/edit/category/(?P<dk>\d+)/$', edit_products_category, name="edit_product_category"),
    re_path(r'^products/edit/(?P<dk>\d+)/$',edit_product_id, name="edit_product_id"),


    re_path(r'^movements/$', movements,name ="movements"),
    re_path(r'^movements/new_order/add_product/$', add_product_to_order,name ="new_order_add_product"),
    re_path(r'^movements/edit_orders/vendor/(?P<dk>\d+)/$', edit_order_vendor, name ="edit_order_vendor"),
    re_path(r'^movements/edit_orders/vendor/edit/(?P<dk>\d+)/$', edit_order_id, name ="edit_order_id"),
    re_path(r'^movements/edit_orders/item_order/(?P<dk>\d+)/$', edit_item_order_id, name ="edit_itemorder_id"),

    re_path(r'^movements/all_orders/$', all_orders, name ="all_orders"),
    re_path(r'^movements/all_orders/vendor//$', all_orders_vendor, name ="all_orders_vendor"),
    re_path(r'^movements/all_orders/(?P<dk>\d+)/$', all_order_id, name ="all_order_id"),
    re_path(r'^movements/all_orders/edit_order/$', edit_order, name ="edit_order"),



]