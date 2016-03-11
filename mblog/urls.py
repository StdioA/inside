from django.conf.urls import include, url
import views
import api

app_name = 'mblog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^(?P<pk>\d+)$', views.PostView.as_view(), name='post'),
    url(r'^(?P<pk>\d+)$', views.view_post, name='post'),
    # url(r'^spa/\d', views.spa_post, name="spa_post"),
    url(r'^(?P<post_id>\d+)/comment$', views.add_comment, name='add_comment'),
    url(r'^api/verify', views.verify, name='verify'),
    url(r'^api/(?P<post_id>\d+)/comment$', api.comment, name='api_comment'),
    url(r'^api/(?P<post_id>\d+)/(post)?$', api.post, name='api_post'),
]
