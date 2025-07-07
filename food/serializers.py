from rest_framework import serializers
from . import models
from decimal import Decimal


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Collection
        fields = ['id', 'name', 'featured_food','total_foods']
    
    total_foods = serializers.IntegerField(read_only=True)




class FoodSerializer(serializers.ModelSerializer):
    
    price_with_tax = serializers.SerializerMethodField()

    class Meta:
        model = models.Food
        fields = ['id', 'title', 'description','slug', 'price', 'price_with_tax', 'collection']
        

    def get_price_with_tax(self, food:models.Food):
        return food.price * Decimal(1.1)
        

 
class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reviews
        fields = ['id', 'user', 'description', 'created_at']

   

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Food
        fields = ['id', 'title','description', 'price']


class CartItemSerializer(serializers.ModelSerializer):
    food = FoodItemSerializer()
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = models.CartItem
        fields = ['id', 'food', 'quantity','total_price']
    
    def get_total_price(self, cart_item:models.CartItem):
        return cart_item.quantity * cart_item.food.price



class CartSerializer(serializers.ModelSerializer):
    cart_id = serializers.UUIDField(read_only=True)
    cart_items= CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart:models.Cart):
        return sum( cart_item.quantity * cart_item.food.price for cart_item in cart.cart_items.all())


    class Meta:
        model = models.Cart
        fields = ['cart_id', 'created_at', 'cart_items','total_price']