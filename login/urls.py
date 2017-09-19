from django.conf.urls import url

from . import views

app_name = 'login'
urlpatterns = [
    url(r'^$', views.login, name='indexlogin'),

    url(r'^login/$', views.login, name='login'),
]