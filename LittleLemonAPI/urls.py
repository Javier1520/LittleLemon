from django.urls import path
from . import views

urlpatterns = [
    path('categories', views.CategoryView.as_view(), name='categories'),
    path('categories/<int:pk>', views.SingleCategoryView.as_view(), name='single-category'),
    path('menu-items', views.MenuItemView.as_view(), name='menu-items'),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view(), name='single-menu-item'),
    path('cart/menu-items', views.CartView.as_view(), name='cart'),
    path('orders', views.OrderView.as_view(), name='orders'),
    
    #M groups
    path('groups/manager/users', views.ManagerView.as_view(), name='manager-users'),
    path('groups/manager/users/<int:pk>', views.SingleManagerView.as_view(), name='single-manager'),
    path('delivery-crew/users', views.DeliveryCrewView.as_view(), name='delivery-crew-users'),
    path('delivery-crew/users/<int:pk>', views.SingleDeliveryCrewView.as_view(), name='single-delivery-crew'),
]