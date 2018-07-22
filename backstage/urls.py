from django.conf.urls import include, url
from . import views

app_name = 'backstage'
urlpatterns = [
    url(r'^data/import/?$', views.import_data, name='import-data'),
    url(r'^data/export/?$', views.export_data, name='export-data'),
    url(r'^data/?$', views.index, name='data'),
]
