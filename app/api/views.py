from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend


from api.mixins import ListViewSet
from lesson.models import UserLesson, UserProduct, Product
from api.serializers import (
    UserLessonSerializer, ProductSerializer, UserLessonDateLastSerializer
)
from api.filter import ProductFilter


class UserListViewSet(ListViewSet):
    """Вьюсет для UserLesson."""
    queryset = UserLesson.objects.all()
    serializer_class = UserLessonSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter

    def get_serializer_class(self):
        if self.request.query_params:
            return UserLessonDateLastSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(
            user=user,
            lesson__product__in=UserProduct.objects.filter(
                user=user
            ).values('product')
        )


class ProductViewSet(ListViewSet):
    """Вьюсет для Product."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)
