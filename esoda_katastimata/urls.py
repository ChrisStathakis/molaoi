from django.urls import re_path
from .views import *




urlpatterns =[
    re_path(r'^$',view=homepage),
    re_path(r'active-month/$',view=create_new_month),
    re_path(r'deactive-month/$',view=deactive_month),
    re_path(r'active-year/$',view=create_new_year),
    re_path(r'deactive-year/$',view=deactive_year),
    re_path(r'new-esoda/$',view=new_esoda),
    re_path(r'esodo/(?P<dk>\d+)/$',view=edit_day),

    re_path(r'income/year/(?P<yk>\d+)/$',view=esoda_income_choose_year),
    re_path(r'income/month/(?P<mk>\d+)/$',view=esoda_income_choose_month),



    ]
