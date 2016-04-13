from django.conf.urls import include, url
import data

app_name = 'backstage'
urlpatterns = [
    url(r'^data/import/?$', data.import_data, name='import-data'),
    url(r'^data/inside-data.json$', data.export_data, name='export-data'),
    url(r'^data/?$', data.data, name='data'),
]
