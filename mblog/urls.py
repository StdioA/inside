from django.conf.urls import include, url
import views
import api
import auth

app_name = 'mblog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^(?P<pk>\d+)$', views.PostView.as_view(), name='post'),
    url(r'^0$', views.manage_post, name='manage'),
    url(r'^login', auth.user_login, name='login'),
    url(r'^logout', auth.user_logout, name='logout'),
    url(r'^(?P<pk>\d+)$', views.view_post, name='post'),
    url(r'^(?P<post_id>\d+)/comment$', views.add_comment, name='add_comment'),
    url(r'^api/(?P<post_id>\d+)/comment$', api.comment, name='api_comment'),
    url(r'^api/(?P<post_id>\d+)/(post)?$', api.post, name='api_post'),
]
