from djoser.serializers import UserCreateSerializer, UserSerializer
from users.models import User


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = (
                  'email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  )
        model = User