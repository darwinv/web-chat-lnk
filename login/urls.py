from django.conf.urls import url

from . import views

app_name = 'login'
urlpatterns = [

    # login
    # ingreso por defecto
    url(r'^$', views.weblogin, name='indexlogin'),

    # requerido por Django para cuando rechazar un request de un
    # usuario que no esta autorizado
    url(r'^accounts/login/$', views.weblogin, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/', views.logout_view, name='logout'),
]
