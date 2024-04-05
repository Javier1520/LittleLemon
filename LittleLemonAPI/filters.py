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

# class OrderFilter(django_filters.FilterSet):
#     status = django_filters.BooleanFilter(field_name='status', lookup_expr='exact')
#     total = django_filters.NumberFilter(lookup_expr='exact')
#     date = django_filters.DateTimeFilter(lookup_expr='exact')

#     class Meta:
#         model = Order
#         fields = ['status', 'total', 'date']


# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="delivery_crew", null=True)
#     status = models.BooleanField(db_index=True, default=0)
#     total = models.DecimalField(max_digits=6, decimal_places=2)
#     date = models.DateTimeField(db_index=True, auto_now_add=True)