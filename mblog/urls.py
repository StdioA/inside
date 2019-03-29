from django.conf.urls import url
from . import views
from . import auth


app_name = 'mblog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^0$', views.add_post, name='add'),
    url(r'^login/?$', auth.user_login, name='login'),
    url(r'^logout/?$', auth.user_logout, name='logout'),
    url(r'^archive/?$', views.archive, name='archive'),
    url(r'^(?P<pk>\d+)$', views.view_post, name='post'),
]
