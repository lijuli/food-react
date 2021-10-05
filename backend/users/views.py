from rest_framework.pagination import PageNumberPagination
from users.models import User
from users.serializers.user_serializer import CustomUserSerializer
from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
User = get_user_model()


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()
    pagination_class = PageNumberPagination

