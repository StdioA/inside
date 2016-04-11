from django.conf.urls import include, url
import views
import api
import auth

app_name = 'mblog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^(?P<pk>\d+)$', views.PostView.as_view(), name='post'),
    url(r'^0$', views.add_post, name='add'),
    url(r'^login', auth.user_login, name='login'),
    url(r'^logout', auth.user_logout, name='logout'),
    url(r'^archive', views.archive, name='archive'),
    url(r'^(?P<pk>\d+)$', views.view_post, name='post'),
    # url(r'^api/latest$', api.get_latest, name='api_latest'),                  # DEPRECATED
    url(r'^api/comment/(?P<post_id>\d+)/?$', api.comment, name='api_comment'),
    url(r'^api/(post/)?(?P<post_id>\d+)/?$', api.post, name='api_post'),
    url(r'^api/archive/((?P<post_id>\d+)/)?((counts/)(?P<number>\d+)/)?$', api.archive, name='api_archive'),
]
