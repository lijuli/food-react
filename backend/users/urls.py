from django.conf.urls import url, include
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users import views

router_v1 = DefaultRouter()
#
# router_v1.register(r'(?P<user_id>[0-9]+)/subscribe',
#                    views.SubscribeViewSet,
#                    basename='subscribe_api')
# router_v1.register(r'subscriptions',
#                    views.SubscriptionViewSet,
#                    basename='subscription_api')
router_v1.register(r'', views.CustomUserViewSet)

urlpatterns = [
    path('api/users/', include(router_v1.urls)),
    # url(r'^api/v1/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken'))
]
