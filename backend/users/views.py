from rest_framework.pagination import PageNumberPagination
from users.models import User, Subscription
# from users.serializers.subscription_serializer import SubscribeSerializer
from users.serializers.user import CustomUserSerializer
from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
User = get_user_model()
from rest_framework.views import APIView
from users.serializers.subscription import SubscribeSerializer


class CustomUserViewSet(UserViewSet):
    pagination_class = PageNumberPagination

    @action(
        detail=False,
        methods=['get'],
        url_path='subscriptions'
    )
    def get_subscriptions(self, request):
        users = User.objects.filter(subscribed__user=self.request.user)
        page = self.paginate_queryset(users)
        serializer = SubscribeSerializer(
            # page,
            many=True,
            instance=users,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['get', 'delete'],
        url_path='subscribe'
    )
    def subscribe(self, request, id=None):
        current_user = request.user
        user = get_object_or_404(
            User,
            id=id
        )

        if request.method == 'GET':

            if Subscription.objects.filter(subscribed=current_user, user=user).exists():
                return Response(status=status.HTTP_204_NO_CONTENT)

            serializer = SubscribeSerializer(
                many=False,
                instance=user,
                context={'request': request}
            )
            Subscription.objects.create(user_id=id, subscribed=current_user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        Subscription.objects.filter(subscribed_id=current_user.id, user_id=user.id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
