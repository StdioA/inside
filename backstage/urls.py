from django.conf.urls import url
from . import views


app_name = 'backstage'
urlpatterns = [
    url(r'^data/import/?$', views.DataImportView.as_view(),
        name='import-data'),
    url(r'^data/export/?$', views.DataExportView.as_view(),
        name='export-data'),
    url(r'^data/?$', views.index, name='data'),
]
