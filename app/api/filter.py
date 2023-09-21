import django_filters

from lesson.models import UserLesson


class ProductFilter(django_filters.FilterSet):
    """Класс FilterSet для фильтрации по продукту."""
    product = django_filters.CharFilter(field_name='lesson__product__name')

    class Meta:
        model = UserLesson
        fields = (
            'product',
        )
