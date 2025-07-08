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

class AddItemSerializer(serializers.ModelSerializer):
    food_id = serializers.IntegerField()
    class Meta:
        model = models.CartItem
        fields = ['id', 'food_id', 'quantity'] 

    def validate_food_id(self, value):
        if not models.Food.objects.filter(pk=value).exists():
            raise serializers.ValidationError("No product with the given ID was found.")
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        food_id = self.validated_data['food_id']
        quantity = self.validated_data['quantity']
        

        try: 
            cart_item = models.CartItem.objects.get(
                cart_id = cart_id,
                food_id = food_id
            )
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
            

        except models.CartItem.DoesNotExist:
            cart_item = models.CartItem.objects.create(
                cart_id = cart_id,
                **self.validated_data
            )
            self.instance = cart_item
        return self.instance
    


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = ['quantity']

class CartItemSerializer(serializers.ModelSerializer):
    food = FoodItemSerializer(read_only=True)
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


class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = models.User
        fields = ['id','user_id', 'phone_no', 'birthdate', 'membership']