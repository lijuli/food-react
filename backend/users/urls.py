from django.conf.urls import url, include
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users import views

router_v1 = DefaultRouter()
router_v1.register(r'', views.CustomUserViewSet)

urlpatterns = [
    path('api/users/', include(router_v1.urls)),
    url(r'^auth/', include('djoser.urls.authtoken'))
]
