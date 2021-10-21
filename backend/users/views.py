from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipes.permissions import IsAuthorOrAdmin
from recipes.views import DefaultResultsSetPagination
from users.models import Subscription, User
from users.serializers.subscription import SubscribeSerializer, SubscriptionsSerializer


class CustomUserViewSet(UserViewSet):
    pagination_class = DefaultResultsSetPagination
    action_permissions = {
        IsAuthorOrAdmin: ['partial_update', 'destroy', 'create'],
        AllowAny: ['retrieve', 'list']
    }

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
        url_path='subscriptions'
    )
    def get_subscriptions(self, request):
        current_user = self.request.user
        paginator = DefaultResultsSetPagination()
        subscriptions = Subscription.objects.filter(subscribed=current_user)
        result_page = paginator.paginate_queryset(subscriptions, request)
        serializer = SubscriptionsSerializer(
            result_page,
            many=True,
            context={
                'request': request
            }
        )
        return paginator.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['get', 'delete'],
        permission_classes=[IsAuthenticated],
        url_path='subscribe'
    )
    def subscribe(self, request, id=None):
        current_user = request.user
        user = get_object_or_404(
            User,
            id=id
        )
        if request.method == 'GET':
            if Subscription.objects.filter(
                    subscribed=current_user, user=user
            ).exists():
                return Response(status=status.HTTP_204_NO_CONTENT)
            serializer = SubscriptionsSerializer(
                data={
                    'user': user.id,
                    'subscribed': current_user.id
                    # 'user': current_user.id,
                    # 'subscribed': user.id
                },
                context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        Subscription.objects.filter(
            subscribed_id=current_user.id,
            user_id=user.id
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
