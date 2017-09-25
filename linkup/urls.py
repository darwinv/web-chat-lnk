from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns


urlpatterns = i18n_patterns(
    #login
    url(r'^', include('login.urls')),

    #admin linkup
    url(r'^admin/', include('dashboard.urls')),
)