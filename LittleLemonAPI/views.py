from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth.models import User, Group
from .models import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .serializers import *
from rest_framework import status

# Category views
class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({'message': 'Only managers can create categories'}, status=status.HTTP_403_FORBIDDEN)

        return super().create(request, *args, **kwargs)

class SingleCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({'message': 'Only managers can update categories'}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({'message': 'Only managers can delete categories'}, status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)

# MenuItem views
class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({'message': 'Only managers can create menu items'}, status=status.HTTP_403_FORBIDDEN)

        return super().create(request, *args, **kwargs)

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({'message': 'Only managers can update menu items'}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({'message': 'Only managers can delete menu items'}, status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)

# User group managent
class ManagerView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({'message': 'Only managers can access'}, status=status.HTTP_403_FORBIDDEN)
        return super().get(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({'message': 'Only managers can access'}, status=status.HTTP_403_FORBIDDEN)
        manager_group = Group.objects.get(name='Manager')
        user = get_object_or_404(User, username=request.data.get('username'))
        manager_group.user_set.add(user)
        return Response({'message': 'User added to manager group'})

class SingleManagerView(generics.DestroyAPIView):
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, pk, *args, **kwargs):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({'message': 'Only managers can access'}, status=status.HTTP_403_FORBIDDEN)
        manager_group = Group.objects.get(name='Manager')
        user = get_object_or_404(User, pk=pk)
        manager_group.user_set.remove(user)
        return Response({'message': 'User removed from manager group'})

class DeliveryCrewView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name='Delivery crew')
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({'message': 'Only managers can access'}, status=status.HTTP_403_FORBIDDEN)
        return super().get(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({'message': 'Only managers can access'}, status=status.HTTP_403_FORBIDDEN)
        delivery_crew_group = Group.objects.get(name='Delivery crew')
        user = get_object_or_404(User, username=request.data.get('username'))
        delivery_crew_group.user_set.add(user)
        return Response({'message': 'User added to delivery crew group'})

class SingleDeliveryCrewView(generics.DestroyAPIView):
    queryset = User.objects.filter(groups__name='Delivery crew')
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, pk, *args, **kwargs):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({'message': 'Only managers can access'}, status=status.HTTP_403_FORBIDDEN)
        delivery_crew_group = Group.objects.get(name='Delivery crew')
        user = get_object_or_404(User, pk=pk)
        delivery_crew_group.user_set.remove(user)
        return Response({'message': 'User removed from delivery crew group'})

class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response({'message': 'Item already in cart'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        cart = Cart.objects.filter(user=user)
        cart.delete()
        return Response({'message': 'Cart cleared'})

class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            return super().get(request, *args, **kwargs)
        elif request.user.groups.filter(name='Delivery crew').exists():
            orders_to_deliver = Order.objects.filter(delivery_crew=request.user)
            serializer = OrderSerializer(orders_to_deliver, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            customer_orders = Order.objects.filter(user=request.user)
            serializer = OrderSerializer(customer_orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        carts = Cart.objects.filter(user=self.request.user)
        total = sum(cart.price for cart in carts)

        order = serializer.save(total=total, user=self.request.user)
        for cart in carts:
            order_item = OrderItem.objects.create(
                order=order,
                menuitem=cart.menuitem,
                quantity=cart.quantity,
                unit_price=cart.unit_price,
                price=cart.price
            )
            cart.delete()

        return serializer.instance

class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            exac_order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(exac_order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.user.groups.filter(name='Delivery crew').exists():
            orders_to_deliver = Order.objects.filter(delivery_crew=request.user, pk=pk)
            serializer = OrderSerializer(orders_to_deliver, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            customer_orders = Order.objects.filter(user=request.user)
            serializer = OrderSerializer(customer_orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)