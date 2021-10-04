from django.urls import include, path
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()
# router_v1.register("ingridients", IngridientViewSet, basename="ingridient_api")
# router_v1.register(
#     r"titles/(?P<title_id>[0-9]+)/reviews",
#     ReviewViewSet,
#     basename="review_api",
# )
# router_v1.register(
#     (
#         r"titles/(?P<title_id>[0-9]+)"
#         r"/reviews/(?P<review_id>[0-9]+)/comments"
#     ),
#     CommentViewSet,
#     basename="comment_api",
# )
# router_v1.register("categories", CategoryViewSet, basename="category_api")
# router_v1.register("genres", GenreViewSet, basename="genre_api")

urlpatterns = [
    path("v1/", include(router_v1.urls)),
]
