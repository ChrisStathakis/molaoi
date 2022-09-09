from django.urls import re_path
from .views import *


urlpatterns=[
    re_path(r'^$',view=homepage),
    re_path(r'^προιόντα/$',view=products),
    re_path(r'^προιόντα/activate/(?P<dk>\d+)/$',view=activate_deactivate_product),

    re_path(r'^προιόντα/δημιουργία/$',view=create_product),
    re_path(r'^προιόντα/επεξεργασία/vendoras/',view=create_vendor_from_product),
    re_path(r'^προιόντα/επεξεργασία/(?P<dk>\d+)/$',view=edit_product),

    re_path(r'^προιόντα/δημιουργία/add_only_color/(?P<dk>\d+)/$',view=add_only_color_to_product),
    re_path(r'^προιόντα/δημιουργία/add_color/(?P<dk>\d+)/$',view=add_color_and_size),
    re_path(r'^προιόντα/δημιουργία/add_color/(?P<dk>\d+)/(?P<pk>\d+)/$',view=add_size_to_color),
    re_path(r'^προιόντα/δημιουργία/delete-size/(?P<dk>\d+)/(?P<pk>\d+)/$',view=delete_size),


    re_path(r'^προμηθευτές/$',view=vendors),
    re_path(r'^προμηθευτές/δημιουργία/$',view=create_vendor),
    re_path(r'^προμηθευτές/επεξεργασία/(?P<dk>\d+)/$',view=edit_vendor),

    re_path(r'^προμηθευτές/διαχείρηση-επιταγών/$',view=check_orders_management),
    re_path(r'^προμηθευτές/διαχείρηση-επιταγών/(?P<dk>\d+)/$',view=edit_check_order),

    re_path(r'^προμηθευτές/προκαταβολή/(?P<dk>\d+)/$',view=vendor_deposit_order),
    re_path(r'^προμηθευτές/επιταγή/(?P<dk>\d+)/$',view=vendor_check_order),
    re_path(r'^προμηθευτές/επιταγή/(?P<dk>\d+)/είσπραξη/$',view=payment_check),


    re_path(r'^τιμολόγια/$',view=orders),
    re_path(r'^τιμολόγια/νέο/$',view=create_order),
    re_path(r'^τιμολόγια/προμηθευτής/$',view=create_vendor_from_order),




    re_path(r'^εργαλεία/$',view=tools),
    re_path(r'^εργαλεία/payment_group/(?P<dk>\d+)$',view=edit_payment_group),
    re_path(r'^εργαλεία/payment/(?P<dk>\d+)$',view=edit_payment),

    re_path(r'^εργαλεία/(?P<dk>\d+)/$',view=activate_or_deactive_color),
    re_path(r'^εργαλεία/edit/(?P<dk>\d+)/$',view=tools_edit_color),
    re_path(r'^εργαλεία/size/(?P<dk>\d+)/$',view=activate_deactivate_size),
    re_path(r'^εργαλεία/size/edit/(?P<dk>\d+)/$',view=tools_edit_size),


    re_path(r'^εργαλεία/αλλαγή-ποσότητας/δημιουργία/$',view=tools_change_order),
    re_path(r'^εργαλεία/αλλαγή-ποσότητας/(?P<dk>\d+)/$',view=tools_change_qty),
    re_path(r'^εργαλεία/αλλαγή-ποσότητας/(?P<dk>\d+)/(?P<pk>\d+)$',view=tools_grab_qty),
    re_path(r'^εργαλεία/αλλαγή-ποσότητας/color/(?P<dk>\d+)/(?P<pk>\d+)$',view=tools_grab_color),
    re_path(r'^εργαλεία/αλλαγή-ποσότητας/size/(?P<dk>\d+)/(?P<pk>\d+)$',view=tools_grab_size),

    re_path(r'^τιμολόγια/DOY/$',view=create_taxes_city),

    re_path(r'^τιμολόγια/επεξεργασία/(?P<dk>\d+)/$',view=order_edit_id),

    #add on order items urls
    re_path(r'^τιμολόγια/check/(?P<dk>\d+)/(?P<pk>\d+)/$',view=add_product_to_order),
    re_path(r'^τιμολόγια/check/(?P<dk>\d+)/(?P<pk>\d+)/size/(?P<ck>\d+)/$',view=create_size_to_color_from_order),
    re_path(r'^τιμολόγια/check/(?P<dk>\d+)/(?P<pk>\d+)/(?P<ck>\d+)/$',view=add_size_to_order_item),
    re_path(r'^τιμολόγια/check/(?P<dk>\d+)/(?P<pk>\d+)/(?P<ck>\d+)/(?P<sk>\d+)/$',view=add_color_and_size_to_order_item),
    re_path(r'^τιμολόγια/check/only-color/(?P<dk>\d+)/(?P<pk>\d+)/(?P<ck>\d+)/$',view=add_only_color_to_order_item),



    re_path(r'^τιμολόγια/επεξεργασία-προϊόντος/(?P<dk>\d+)/(?P<pk>\d+)/$',view=edit_product_from_order),

    re_path(r'^τιμολόγια/διαγραφή/(?P<dk>\d+)/$',view=done_order_delete_id),
    re_path(r'^τιμολόγια/(?P<dk>\d+)/επεξεργασία/$',view=order_edit),
    re_path(r'^τιμολόγια/προσθήκη-προιόντος/(?P<dk>\d+)/$',view=create_product_from_order_page),
    re_path(r'^τιμολόγια/προσθήκη-προιόντος/(?P<ok>\d+)/color/(?P<pk>\d+)/$',view=choose_color_to_product_from_order),
    re_path(r'^τιμολόγια/επεξεργασία-προϊόντος/add-color/(?P<ok>\d+)/(?P<pk>\d+)/(?P<ck>\d+)/$',view=add_size_to_product_from_order),
    re_path(r'^τιμολόγια/προσθήκη-προιόντος/(?P<dk>\d+)/cat$',view=create_category_from_order),
    re_path(r'^τιμολόγια/διαγραφή-προιόντος/(?P<dk>\d+)/$',view=delete_order_item),






]




