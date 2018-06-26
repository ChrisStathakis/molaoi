from django.conf.urls import url
from recipes.views import *


urlpatterns =[
    url(r'^$',view=homepage),
    url(r'^νέα/$',view=new_recipe),
    url(r'κατηγορία/(?P<dk>\d+)/$',view=recipes_per_category),
    url(r'κατηγορία/(?P<dk>\d+)/ap/(?P<pk>\d+)$',view=activate_deactivate_recipe),
    url(r'προσθήκη/(?P<dk>\d+)/$',view=add_product_to_recipe),
    url(r'επεξεργασία-συνταγής/(?P<dk>\d+)/$',view=edit_recipe_id),
    url(r'προσθήκη-συστατικού/(?P<dk>\d+)/$',view=choose_product_to_recipe),
    url(r'^επεξεργασία-συστατικού/(?P<dk>\d+)/(?P<pk>\d+)/$',view=edit_recipe_item_id),

    url(r'κατηγορίες/$',view=recipe_categories),
    url(r'κατηγορίες/(?P<dk>\d+)/$',view=edit_recipe_categories),












]
