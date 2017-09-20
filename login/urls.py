from django.conf.urls import url

from . import views

app_name = 'login'
urlpatterns = [
    url(r'^$', views.weblogin, name='indexlogin'),

    url(r'^accounts/login/$', views.weblogin, name='login'),
]