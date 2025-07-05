from django.contrib import admin
from food.admin import FoodAdmin
from tags.models import TaggedItem
from django.contrib.contenttypes.admin import GenericTabularInline
from food.models import Food


class TagInline(GenericTabularInline):
    model = TaggedItem
    extra = 0
    min_num = 1
    # autocomplete_fields = ['tag']
   
    
class CustomFoodAdmin(FoodAdmin):
    inlines = [TagInline]

admin.site.unregister(Food)
admin.site.register(Food, CustomFoodAdmin)