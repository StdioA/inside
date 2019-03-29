from django.conf.urls import url
from . import views


app_name = 'api'
urlpatterns = [
    url(r'^comment/(?P<post_id>\d+)/?$', views.CommentView.as_view(),
        name='api-comment'),
    url(r'^(post/)?(?P<post_id>\d+)/?$', views.PostView.as_view(),
        name='api-post'),
    url(r'^archive/((?P<post_id>\d+)/)?((counts/)(?P<number>\d+)/)?$',
        views.ArchiveView.as_view(), name='api-archive'),
]
