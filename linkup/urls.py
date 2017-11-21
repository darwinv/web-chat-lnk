from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns

from api.connection import api

urlpatterns = i18n_patterns(
    #login
    url(r'^', include('login.urls')),
    #admin linkup
    url(r'^admin/', include('dashboard.urls')),

)


urlpatterns += [
	#api web
	url(r'^api/', include('api.urls')),
]