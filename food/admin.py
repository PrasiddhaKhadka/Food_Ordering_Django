from django.contrib import admin
from django.db.models.query import QuerySet
from django.db.models import Count
from django.http import HttpRequest
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import F, ExpressionWrapper, DecimalField
from . import models
from tags.models import TaggedItem
from django.contrib.contenttypes.admin import GenericTabularInline

           

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name','featured_food','total_foods']
    list_per_page = 5
    list_filter = ['name']
    search_fields = ['name__istartswith','last_update']
    

    def total_foods(self, collection:models.Collection):
        url = reverse('admin:food_food_changelist') + f'?collection__id__exact={collection.id}'
        return format_html('<a href="{}">{}</a>',url, collection.total_foods)
        # return collection.total_foods
    
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(total_foods=Count('food'))





@admin.register(models.Food)
class FoodAdmin(admin.ModelAdmin):
    actions = ['upd_price']
    list_display = ['title', 'price', 'collection','top_sale']
    list_per_page = 5
    list_editable = ['price']
    list_filter = ['collection']
    list_select_related = ['collection']
    search_fields = ['title__istartswith']
    prepopulated_fields ={
        'slug': ['title'],
    }
    autocomplete_fields = ['collection']
 


    def top_sale(self, food:models.Food):
        if food.price > 100:
            return 'Yes'
        return 'No'
    

    @admin.action(description='Update price by 10%%')
    def upd_price(self, request, queryset):
        updated_price = ExpressionWrapper(F('price') * 1.1, output_field=DecimalField())
        queryset.update(price=updated_price)
        self.message_user(request, 'Price updated')



@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['food', 'order', 'quantity']
    search_fields = ['food__title']


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 0
    min_num = 1
    max_num = 10
    autocomplete_fields = ['food']

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'placed_at']
    inlines = [OrderItemInline]
    

@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'food', 'quantity']
    autocomplete_fields = ['food']