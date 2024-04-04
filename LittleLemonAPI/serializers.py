from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueTogetherValidator

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'slug', 'title')
        validators = [
            UniqueTogetherValidator(
                queryset=Category.objects.all(),
                fields=('slug','title'),
            ),
        ]

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = ('id', 'title', 'price', 'featured', 'category', 'category_id')

class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Cart
        fields = ('id', 'user', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price')

    def create(self, validated_data):
        menuitem_id = validated_data.pop('menuitem_id')
        quantity = validated_data.get('quantity')

        try:
            menuitem = MenuItem.objects.get(pk=menuitem_id)
        except MenuItem.DoesNotExist:
            raise serializers.ValidationError("Invalid MenuItem primary key.")

        validated_data['menuitem'] = menuitem
        validated_data['unit_price'] = menuitem.price
        validated_data['price'] = menuitem.price * quantity
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['unit_price'] = instance.unit_price
        representation['price'] = instance.price
        return representation

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_id = serializers.IntegerField(read_only=True)
    total = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    status = serializers.BooleanField(read_only=True)
    delivery_crew = serializers.ReadOnlyField(source='delivery_crew.username')
    delivery_crew_id = serializers.IntegerField(read_only=True)
    date = serializers.DateTimeField(read_only=True, format="%d/%m/%Y - %H:%M:%S")
    order_items = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user','user_id', 'delivery_crew','delivery_crew_id', 'status', 'total', 'date', 'order_items')

class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    order_id = serializers.IntegerField(write_only=True)
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'order_id', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')