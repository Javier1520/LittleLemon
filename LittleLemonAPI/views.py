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
            orders = Order.objects.all()
        elif request.user.groups.filter(name='Delivery crew').exists():
            orders = Order.objects.filter(delivery_crew=request.user)
        else:
            orders = Order.objects.filter(user=request.user)

        # Fetch order items for each order
        orders_with_items = []
        for order in orders:
            order_items = OrderItem.objects.filter(order=order)
            order_item_serializer = OrderItemSerializer(order_items, many=True)
            order_data = OrderSerializer(order).data
            order_data['order_items'] = order_item_serializer.data
            orders_with_items.append(order_data)
        return Response(orders_with_items, status=status.HTTP_200_OK)

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
            exac_order = get_object_or_404(Order,pk=pk)
            serializer = OrderSerializer(exac_order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.user.groups.filter(name='Delivery crew').exists():
            orders_to_deliver = Order.objects.filter(delivery_crew=request.user, pk=pk)
            serializer = OrderSerializer(orders_to_deliver, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            customer_order = get_object_or_404(Order, user=request.user, pk=pk)
            order_serializer = OrderSerializer(customer_order)
            customer_orderitems = OrderItem.objects.filter(order=pk)
            orderitem_serializer = OrderItemSerializer(customer_orderitems, many=True)
            order_data = order_serializer.data
            order_data['order_items'] = orderitem_serializer.data
            return Response(order_data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            if 'delivery_crew_id' in request.data:
                order = get_object_or_404(Order, pk=pk)
                delivery = get_object_or_404(User, pk=request.data['delivery_crew_id'])
                if delivery.groups.filter(name='Delivery crew').exists():
                    order.delivery_crew_id = request.data['delivery_crew_id']
                    order.save()
                    return Response(OrderSerializer(order).data, status= status.HTTP_200_OK)
                return Response({'message': 'Invalid delivery crew'}, status=status.HTTP_400_BAD_REQUEST)
        elif request.user.groups.filter(name='Delivery crew').exists():
            order = get_object_or_404(Order.objects.filter(delivery_crew=request.user, pk=pk))
            if order.status == 0:
                order.status = 1
                order.save()
                return Response({'message': 'Order status updated to "Delivered"'}, status=status.HTTP_200_OK)
            return Response({'message': 'Order status already updated'}, status=status.HTTP_200_OK)
        else:
            return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({'message': 'Only managers can delete orders'}, status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)