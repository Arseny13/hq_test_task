from rest_framework import mixins, viewsets


class ListViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Класс ViewSet только для получения объектов."""
    pass
