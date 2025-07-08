from django.contrib import admin
from food.admin import FoodAdmin
from tags.models import TaggedItem
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from food.models import Food
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "usable_password", "password1", "password2",'email','first_name','last_name'),
            },
        ),
    )

class TagInline(GenericTabularInline):
    model = TaggedItem
    extra = 0
    min_num = 1
    # autocomplete_fields = ['tag']
   
    
class CustomFoodAdmin(FoodAdmin):
    inlines = [TagInline]

admin.site.unregister(Food)
admin.site.register(Food, CustomFoodAdmin)