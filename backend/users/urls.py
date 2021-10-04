from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/v1/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken'))
]

