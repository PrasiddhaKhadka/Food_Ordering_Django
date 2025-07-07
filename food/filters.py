from django_filters.rest_framework import FilterSet
from . import models

class FoodFilter(FilterSet):
    class Meta:
        model = models.Food
        fields = {
            'collection_id': ['exact'],
            'price': ['gt', 'lt'],
            
        }