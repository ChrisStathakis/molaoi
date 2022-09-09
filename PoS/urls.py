from django.urls import re_path
from .views import *




urlpatterns =[
    re_path(r'^$',view=homepage),
    re_path(r'νέα-παραγγελία/(?P<dk>\d+)/$',view=new_order),
    re_path(r'επέλεξε-συνταγή/(?P<dk>\d+)/$',view=add_products_to_order_main),
    re_path(r'επέλεξε-συνταγή/(?P<dk>\d+)/κατηγορία/(?P<ck>\d+)$',view=add_products_to_order_category),
    re_path(r'επέλεξε-συνταγή/προσθήκη-συνταγής/(?P<dk>\d+)/(?P<ck>\d+)/(?P<pk>\d+)',view=add_recipe_to_order_from_cat),

    re_path(r'επέλεξε-συνταγή/(?P<dk>\d+)/πληρωμή$',view=order_pay_not_complete),






    re_path(r'επέλεξε-συνταγή/προσθήκη-συνταγής/(?P<dk>\d+)/(?P<pk>\d+)',view=add_recipe_to_order),
    re_path(r'επέλεξε-συνταγή/διαγραφή/(?P<dk>\d+)/(?P<pk>\d+)',view=delete_recipe_from_order),
    re_path(r'επέλεξε-συνταγή/edit/(?P<dk>\d+)/(?P<pk>\d+)',view=edit_recipe_from_order),
    re_path(r'πληρωμή/(?P<dk>\d+)/$',view=order_paid),
    re_path(r'εκτύπωση/$',view=print_order_to_kitchen),



    re_path(r'lianiki/$', view=lianiki_section),
    re_path(r'lianiki/create-return/$', view=create_return_order),
    re_path(r'return-products/(?P<dk>\d+)/$', view= return_products),


    re_path(r'lianiki/new-order/$', view=new_lianiki_order),
    re_path(r'lianiki/order/(?P<dk>\d+)/$', view=lianiki_show_categories),
    re_path(r'lianiki/order/(?P<dk>\d+)/(?P<pk>\d+)/$', view=lianiki_choose_category),
    re_path(r'lianiki/order/(?P<dk>\d+)/(?P<pk>\d+)/add/$', view=lianiki_add_product),
    re_path(r'lianiki/order/(?P<dk>\d+)/(?P<pk>\d+)/(?P<sk>\d+)/$', view=lianiki_add_product_with_color),
    re_path(r'lianiki/order/only_color/(?P<dk>\d+)/(?P<pk>\d+)/(?P<sk>\d+)/$', view=lianiki_add_product_with_only_color),


    re_path(r'lianiki/order/(?P<dk>\d+)/(?P<pk>\d+)/edit/$', view=lianiki_edit_order_item),
    re_path(r'lianiki/order/(?P<dk>\d+)/(?P<pk>\d+)/delete/$', view=lianiki_delete_order_item),
    re_path(r'lianiki/order/(?P<dk>\d+)/pay/$', view=lianiki_order_pay_not_complete),
    re_path(r'lianiki/order/(?P<dk>\d+)/closed/$', view=lianiki_order_closed),




    re_path(r'παραγγελίες/$',view=active_orders),
    re_path(r'stats/$',view=total_stats),
    re_path(r'admin/$',view=admin_section),
    re_path(r'admin/deactive-day/$', view=admin_section_deactive_day),
    re_path(r'admin/active-day/$',view= admin_section_create_new_day),

    re_path(r'admin/deactive-month/$', view=admin_section_deactive_month),
    re_path(r'admin/active-month/$',view= admin_section_create_new_month),

    re_path(r'admin/deactive-year/$', view=admin_section_deactive_year),
    re_path(r'admin/active-year/$',view= admin_section_create_new_year),



    ]
