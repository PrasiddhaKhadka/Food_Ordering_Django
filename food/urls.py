from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router = DefaultRouter()
router.register(r'foods', views.FoodViewSet,basename='food')
router.register(r'collections', views.CollectionViewSet)
router.register(r'carts', views.CartViewSet)

food_router = routers.NestedDefaultRouter(router, 'foods', lookup = 'food')
food_router.register(r'reviews', views.ReviewViewSet, basename = 'food-reviews')

# (lookup will be cart_pk)
cart_router = routers.NestedDefaultRouter(router, 'carts', lookup = 'cart')
cart_router.register(r'items', views.CartItemViewSet, basename = 'cart-items')

urlpatterns = router.urls + food_router.urls + cart_router.urls