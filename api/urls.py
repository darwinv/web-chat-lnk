from django.conf.urls import url

from . import views

app_name = 'api'

urlpatterns = [
    # Estados de cuenta   
    url(r'^provinces/$', views.provinces_by_deparment, name='api-provinces'),
    url(r'^districts/$', views.districts_by_province, name='api-districts'),

]