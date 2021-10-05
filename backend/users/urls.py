from django.conf.urls import url, include
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users import views

router_v1 = DefaultRouter()
router_v1.register(r'users', views.CustomUserViewSet)


urlpatterns = [
    path('api/', include(router_v1.urls)),
    # url(r'^api/v1/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken'))
]
