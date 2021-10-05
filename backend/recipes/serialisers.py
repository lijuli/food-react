from djoser.serializers import UserCreateSerializer, UserSerializer
from users.models import User


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ('id',
                  'email',
                  'username',
                  'first_name',
                  'last_name',
                  )
        # model = User


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        # model = User
        fields = ('id',
                  'email',
                  'username',
                  'first_name',
                  'last_name',
                  )



