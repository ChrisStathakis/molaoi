from django.conf.urls import url
from .views import *




urlpatterns =[
    url(r'^$',view=homepage),
    url(r'νέα-παραγγελία/(?P<dk>\d+)/$',view=new_order),
    url(r'επέλεξε-συνταγή/(?P<dk>\d+)/$',view=add_products_to_order_main),
    url(r'επέλεξε-συνταγή/(?P<dk>\d+)/κατηγορία/(?P<ck>\d+)$',view=add_products_to_order_category),
    url(r'επέλεξε-συνταγή/προσθήκη-συνταγής/(?P<dk>\d+)/(?P<ck>\d+)/(?P<pk>\d+)',view=add_recipe_to_order_from_cat),

    url(r'επέλεξε-συνταγή/(?P<dk>\d+)/πληρωμή$',view=order_pay_not_complete),






    url(r'επέλεξε-συνταγή/προσθήκη-συνταγής/(?P<dk>\d+)/(?P<pk>\d+)',view=add_recipe_to_order),
    url(r'επέλεξε-συνταγή/διαγραφή/(?P<dk>\d+)/(?P<pk>\d+)',view=delete_recipe_from_order),
    url(r'επέλεξε-συνταγή/edit/(?P<dk>\d+)/(?P<pk>\d+)',view=edit_recipe_from_order),
    url(r'πληρωμή/(?P<dk>\d+)/$',view=order_paid),
    url(r'εκτύπωση/$',view=print_order_to_kitchen),



    url(r'lianiki/$', view=lianiki_section),
    url(r'lianiki/create-return/$', view=create_return_order),
    url(r'return-products/(?P<dk>\d+)/$', view= return_products),


    url(r'lianiki/new-order/$', view=new_lianiki_order),
    url(r'lianiki/order/(?P<dk>\d+)/$', view=lianiki_show_categories),
    url(r'lianiki/order/(?P<dk>\d+)/(?P<pk>\d+)/$', view=lianiki_choose_category),
    url(r'lianiki/order/(?P<dk>\d+)/(?P<pk>\d+)/add/$', view=lianiki_add_product),
    url(r'lianiki/order/(?P<dk>\d+)/(?P<pk>\d+)/(?P<sk>\d+)/$', view=lianiki_add_product_with_color),
     url(r'lianiki/order/only_color/(?P<dk>\d+)/(?P<pk>\d+)/(?P<sk>\d+)/$', view=lianiki_add_product_with_only_color),


    url(r'lianiki/order/(?P<dk>\d+)/(?P<pk>\d+)/edit/$', view=lianiki_edit_order_item),
    url(r'lianiki/order/(?P<dk>\d+)/(?P<pk>\d+)/delete/$', view=lianiki_delete_order_item),
    url(r'lianiki/order/(?P<dk>\d+)/pay/$', view=lianiki_order_pay_not_complete),
    url(r'lianiki/order/(?P<dk>\d+)/closed/$', view=lianiki_order_closed),




    url(r'παραγγελίες/$',view=active_orders),
    url(r'stats/$',view=total_stats),
    url(r'admin/$',view=admin_section),
    url(r'admin/deactive-day/$', view=admin_section_deactive_day),
    url(r'admin/active-day/$',view= admin_section_create_new_day),

    url(r'admin/deactive-month/$', view=admin_section_deactive_month),
    url(r'admin/active-month/$',view= admin_section_create_new_month),

    url(r'admin/deactive-year/$', view=admin_section_deactive_year),
    url(r'admin/active-year/$',view= admin_section_create_new_year),



    ]
