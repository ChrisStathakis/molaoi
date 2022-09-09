from  django.urls import re_path
from .views import (
    create_user, log_in, auth_view, logged_in, logout, register
)


urlpatterns =(
    re_path(r'^$', create_user, name='create_user'),
    re_path(r'^log_in/$', log_in, name='log_in'),
    re_path(r'^auth_view/$', auth_view, name='auth_view'),
    re_path(r'^logged_in/$', logged_in, name='logged_in'),
    re_path(r'^logout/$',logout, name='logout'),
    re_path(r'^register/$', register, name='register'),
)
