from django_filters import rest_framework as filters

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    title = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Advertisement
        fields = ['creator', 'title', 'status', 'description']