from django.conf.urls import url,patterns
from .views import *


urlpatterns=[
    url(r'^$',view=homepage),
    url(r'^προιόντα/$',view=products),
    url(r'^προιόντα/activate/(?P<dk>\d+)/$',view=activate_deactivate_product),

    url(r'^προιόντα/δημιουργία/$',view=create_product),
    url(r'^προιόντα/επεξεργασία/vendoras/',view=create_vendor_from_product),
    url(r'^προιόντα/επεξεργασία/(?P<dk>\d+)/$',view=edit_product),

    url(r'^προιόντα/δημιουργία/add_only_color/(?P<dk>\d+)/$',view=add_only_color_to_product),
    url(r'^προιόντα/δημιουργία/add_color/(?P<dk>\d+)/$',view=add_color_and_size),
    url(r'^προιόντα/δημιουργία/add_color/(?P<dk>\d+)/(?P<pk>\d+)/$',view=add_size_to_color),
    url(r'^προιόντα/δημιουργία/delete-size/(?P<dk>\d+)/(?P<pk>\d+)/$',view=delete_size),


    url(r'^προμηθευτές/$',view=vendors),
    url(r'^προμηθευτές/δημιουργία/$',view=create_vendor),
    url(r'^προμηθευτές/επεξεργασία/(?P<dk>\d+)/$',view=edit_vendor),

    url(r'^προμηθευτές/διαχείρηση-επιταγών/$',view=check_orders_management),
    url(r'^προμηθευτές/διαχείρηση-επιταγών/(?P<dk>\d+)/$',view=edit_check_order),

    url(r'^προμηθευτές/προκαταβολή/(?P<dk>\d+)/$',view=vendor_deposit_order),
    url(r'^προμηθευτές/επιταγή/(?P<dk>\d+)/$',view=vendor_check_order),
    url(r'^προμηθευτές/επιταγή/(?P<dk>\d+)/είσπραξη/$',view=payment_check),


    url(r'^τιμολόγια/$',view=orders),
    url(r'^τιμολόγια/νέο/$',view=create_order),
    url(r'^τιμολόγια/προμηθευτής/$',view=create_vendor_from_order),




    url(r'^εργαλεία/$',view=tools),
    url(r'^εργαλεία/payment_group/(?P<dk>\d+)$',view=edit_payment_group),
    url(r'^εργαλεία/payment/(?P<dk>\d+)$',view=edit_payment),

    url(r'^εργαλεία/(?P<dk>\d+)/$',view=activate_or_deactive_color),
    url(r'^εργαλεία/edit/(?P<dk>\d+)/$',view=tools_edit_color),
    url(r'^εργαλεία/size/(?P<dk>\d+)/$',view=activate_deactivate_size),
    url(r'^εργαλεία/size/edit/(?P<dk>\d+)/$',view=tools_edit_size),


    url(r'^εργαλεία/αλλαγή-ποσότητας/δημιουργία/$',view=tools_change_order),
    url(r'^εργαλεία/αλλαγή-ποσότητας/(?P<dk>\d+)/$',view=tools_change_qty),
    url(r'^εργαλεία/αλλαγή-ποσότητας/(?P<dk>\d+)/(?P<pk>\d+)$',view=tools_grab_qty),
    url(r'^εργαλεία/αλλαγή-ποσότητας/color/(?P<dk>\d+)/(?P<pk>\d+)$',view=tools_grab_color),
    url(r'^εργαλεία/αλλαγή-ποσότητας/size/(?P<dk>\d+)/(?P<pk>\d+)$',view=tools_grab_size),







    url(r'^τιμολόγια/DOY/$',view=create_taxes_city),

    url(r'^τιμολόγια/επεξεργασία/(?P<dk>\d+)/$',view=order_edit_id),

    #add on order items urls
    url(r'^τιμολόγια/check/(?P<dk>\d+)/(?P<pk>\d+)/$',view=add_product_to_order),
    url(r'^τιμολόγια/check/(?P<dk>\d+)/(?P<pk>\d+)/size/(?P<ck>\d+)/$',view=create_size_to_color_from_order),
    url(r'^τιμολόγια/check/(?P<dk>\d+)/(?P<pk>\d+)/(?P<ck>\d+)/$',view=add_size_to_order_item),
    url(r'^τιμολόγια/check/(?P<dk>\d+)/(?P<pk>\d+)/(?P<ck>\d+)/(?P<sk>\d+)/$',view=add_color_and_size_to_order_item),
    url(r'^τιμολόγια/check/only-color/(?P<dk>\d+)/(?P<pk>\d+)/(?P<ck>\d+)/$',view=add_only_color_to_order_item),



    url(r'^τιμολόγια/επεξεργασία-προϊόντος/(?P<dk>\d+)/(?P<pk>\d+)/$',view=edit_product_from_order),

    url(r'^τιμολόγια/διαγραφή/(?P<dk>\d+)/$',view=done_order_delete_id),
    url(r'^τιμολόγια/(?P<dk>\d+)/επεξεργασία/$',view=order_edit),
    url(r'^τιμολόγια/προσθήκη-προιόντος/(?P<dk>\d+)/$',view=create_product_from_order_page),
    url(r'^τιμολόγια/προσθήκη-προιόντος/(?P<ok>\d+)/color/(?P<pk>\d+)/$',view=choose_color_to_product_from_order),
    url(r'^τιμολόγια/επεξεργασία-προϊόντος/add-color/(?P<ok>\d+)/(?P<pk>\d+)/(?P<ck>\d+)/$',view=add_size_to_product_from_order),
    url(r'^τιμολόγια/προσθήκη-προιόντος/(?P<dk>\d+)/cat$',view=create_category_from_order),
    url(r'^τιμολόγια/διαγραφή-προιόντος/(?P<dk>\d+)/$',view=delete_order_item),






]




