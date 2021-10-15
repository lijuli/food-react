from djoser.serializers import UserCreateSerializer, UserSerializer
from users.models import User, Subscription
from rest_framework import serializers


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')

    class Meta(UserSerializer.Meta):
        fields = (
                  'email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',
                  )
        model = User

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=obj, subscribed=user).exists()
            # return len(obj.subscribed.values('user_id').filter(user_id=user.id)) == 1
