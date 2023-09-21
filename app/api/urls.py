from django.urls import include, path
from rest_framework import routers

from api.views import UserListViewSet, ProductViewSet

app_name = 'api'

router_v1 = routers.DefaultRouter()

router_v1.register(
    'lessons',
    UserListViewSet,
    basename='lessons'
)
router_v1.register(
    'products',
    ProductViewSet,
    basename='products'
)


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router_v1.urls)),
]
