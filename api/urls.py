from django.conf.urls import include, url
from api import api

app_name = 'api'
urlpatterns = [
    url(r'^comment/(?P<post_id>\d+)/?$', api.comment, name='api-comment'),
    url(r'^(post/)?(?P<post_id>\d+)/?$', api.post, name='api-post'),
    url(r'^archive/((?P<post_id>\d+)/)?((counts/)(?P<number>\d+)/)?$', api.archive, name='api-archive'),
]
