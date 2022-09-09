from django.urls import re_path
from recipes.views import *


urlpatterns =[
    re_path(r'^$',view=homepage),
    re_path(r'^νέα/$',view=new_recipe),
    re_path(r'κατηγορία/(?P<dk>\d+)/$',view=recipes_per_category),
    re_path(r'κατηγορία/(?P<dk>\d+)/ap/(?P<pk>\d+)$',view=activate_deactivate_recipe),
    re_path(r'προσθήκη/(?P<dk>\d+)/$',view=add_product_to_recipe),
    re_path(r'επεξεργασία-συνταγής/(?P<dk>\d+)/$',view=edit_recipe_id),
    re_path(r'προσθήκη-συστατικού/(?P<dk>\d+)/$',view=choose_product_to_recipe),
    re_path(r'^επεξεργασία-συστατικού/(?P<dk>\d+)/(?P<pk>\d+)/$',view=edit_recipe_item_id),

    re_path(r'κατηγορίες/$',view=recipe_categories),
    re_path(r'κατηγορίες/(?P<dk>\d+)/$',view=edit_recipe_categories),












]
