from django.db import models
from uuid import uuid4

# Create your models here.
class Collection(models.Model):
    name = models.CharField(max_length=100)
    featured_food = models.ForeignKey('Food', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Food(models.Model):
    title = models.CharField(max_length=100,verbose_name='Product Title')
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # one collection may have multiple foods
    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, null=True, related_name='food') # db maw chai (collection_id) vanera bascha !!!
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class User(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    phone_no = models.CharField(max_length=10)    
    birthdate = models.DateField()
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    def __str__(self):
        return self.phone_no


class Cart(models.Model):
    cart_id = models.UUIDField(primary_key=True, default=uuid4, editable=False, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    # Reverese relationship -> cart_set , food_set
    


class CartItem(models.Model):
    # one cart may have multiple cart items
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    # one food may be in multiple cart items
    food = models.ForeignKey(Food, on_delete=models.CASCADE) # db maw basni vaneko --> food_id
    quantity = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

 

class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    # one customer maw have multiple food orders
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    # reverse_relation => orderitem_set

    def __str__(self) -> str:
        return f'{self.id}'


class OrderItem(models.Model):
    # one order may have multiple order items =>
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # one food may have multiple order items
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        return f'{self.id}'




