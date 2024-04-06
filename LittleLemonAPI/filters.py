import django_filters
from .models import MenuItem, Order

class MenuItemFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    price = django_filters.NumberFilter(lookup_expr='exact')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    featured = django_filters.BooleanFilter(field_name='featured', lookup_expr='exact')
    category_title = django_filters.CharFilter(field_name='category__title', lookup_expr='icontains')
    category_id = django_filters.NumberFilter(field_name='category__id', lookup_expr='exact')

    class Meta:
        model = MenuItem
        fields = ['title', 'min_price', 'max_price', 'featured', 'category_title', 'category_id']