from django.conf.urls import include, url
from backstage import data

app_name = 'backstage'
urlpatterns = [
    url(r'^data/import/?$', data.import_data, name='import-data'),
    url(r'^data/export/?$', data.export_data, name='export-data'),
    url(r'^data/?$', data.data, name='data'),
]
