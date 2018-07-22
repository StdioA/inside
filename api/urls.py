from django.conf.urls import include, url
from . import views

app_name = 'api'
urlpatterns = [
    url(r'^comment/(?P<post_id>\d+)/?$', views.comment, name='api-comment'),
    url(r'^(post/)?(?P<post_id>\d+)/?$', views.post, name='api-post'),
    url(r'^archive/((?P<post_id>\d+)/)?((counts/)(?P<number>\d+)/)?$', views.archive, name='api-archive'),
]
