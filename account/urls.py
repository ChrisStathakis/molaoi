from  django.conf.urls import url, patterns

urlpatterns =(
    url(r'^$','account.views.create_user', name='create_user'),
    url(r'^log_in/$','account.views.log_in', name='log_in'),
    url(r'^auth_view/$','account.views.auth_view', name='auth_view'),
    url(r'^logged_in/$','account.views.logged_in', name='logged_in'),
    url(r'^logout/$','account.views.logout', name='logout'),
    url(r'^register/$','account.views.register', name='register'),
)
