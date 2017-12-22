from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    # login
    url(r'^', include('login.urls')),
    # admin linkup
    url(r'^admin/', include('dashboard.urls')),

    url(r'^specialist/', include('specialist.urls')),
    url(r'^client/', include('client.urls')),
    url(r'^seller/', include('seller.urls')),


)


urlpatterns += [
    # api web
    url(r'^api/', include('api.urls')),
]
