from django.conf.urls import url
from .views import *




urlpatterns =[
    url(r'^$',view=homepage),
    url(r'active-month/$',view=create_new_month),
    url(r'deactive-month/$',view=deactive_month),
    url(r'active-year/$',view=create_new_year),
    url(r'deactive-year/$',view=deactive_year),
    url(r'new-esoda/$',view=new_esoda),
    url(r'esodo/(?P<dk>\d+)/$',view=edit_day),

    url(r'income/year/(?P<yk>\d+)/$',view=esoda_income_choose_year),
    url(r'income/month/(?P<mk>\d+)/$',view=esoda_income_choose_month),



    ]
