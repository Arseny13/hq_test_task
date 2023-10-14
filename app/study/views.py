from django.db.models import Q, F, FilteredRelation
from rest_framework import viewsets, mixins, exceptions
from rest_framework.permissions import IsAuthenticated

from catalog.models import ProductAccess
from study.models import Lesson
from study.serializers import MyLessonSerializer, MyLessonByProductSerializer


def get_product_accesses(user):
    return ProductAccess.objects.filter(
        user=user,
        is_valid=True
    )


class MyLessonsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = MyLessonSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        accesses = get_product_accesses(self.request.user)
        qs = Lesson.objects.filter(
            products__in=accesses.values('product_id')
        ).alias(  # .annotate
            view_info=FilteredRelation(
                'views',
                condition=Q(views__user=self.request.user)
            )
        ).annotate(
            status=F('view_info__status'),
            view_time=F('view_info__view_time')
        )

        return qs


class MyLessonsByProductViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin
):
    serializer_class = MyLessonByProductSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        accesses = get_product_accesses(self.request.user)

        if not (product_id in accesses.values_list('product_id', flat=True)):
            raise exceptions.NotFound

        qs = Lesson.objects.filter(
            products=product_id
        ).alias(  # .annotate
            view_info=FilteredRelation(
                'views',
                condition=Q(views__user=self.request.user)
            )
        ).annotate(
            status=F('view_info__status'),
            view_time=F('view_info__view_time'),
            last_view_datetime=F('view_info__last_view_datetime')
        )

        return qs
