from django.urls import include, path
from rest_framework import routers

from study.views import MyLessonsViewSet, MyLessonsByProductViewSet

router = routers.SimpleRouter()

router.register(
    'my-lessons',
    MyLessonsViewSet,
    'my-lessons'
)

urlpatterns = [
    path(
        'by-product/<int:product_id>/lessons',
        MyLessonsByProductViewSet.as_view({'get': 'list'})
    ),
    path('', include(router.urls)),
]
