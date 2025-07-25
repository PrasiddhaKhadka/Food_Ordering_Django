# Advanced API Concepts
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from food.filters import FoodFilter
from food.pagination import DefaultPagination
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from .serializers import FoodSerializer, CollectionSerializer, ReviewsSerializer, CartSerializer, CartItemSerializer, AddItemSerializer, UpdateCartItemSerializer,UserSerializer
from . import models




class CollectionViewSet(ModelViewSet):
     
    queryset = models.Collection.objects.annotate(total_foods=Count('food')).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        collection = self.get_object()
        if collection.food.count() > 0:
            return Response(
                {'error': 'Collection cannot be deleted because it includes one or more products.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class FoodViewSet(ModelViewSet):
    queryset = models.Food.objects.all()
    serializer_class = FoodSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
    filterset_fields = ['collection_id','price','title']
    filterset_class = FoodFilter
    search_fields = ['title','description']
    ordering_fields = ['price','created_at']
    pagination_class = DefaultPagination


    def get_serializer_context(self):
        return {
            'request': self.request
        }
    
    def destroy(self, request, *args, **kwargs):
            # food = self.get_object()
            if models.OrderItem.objects.filter(food_id = kwargs['pk']).count() > 0:
                return Response(
                    {'error': 'Product cannot be deleted because it is associated with one or more orders.'},
                    status=status.HTTP_405_METHOD_NOT_ALLOWED
                )
            
            return super().destroy(request, *args, **kwargs)




class ReviewViewSet(ModelViewSet):

    serializer_class = ReviewsSerializer

    def get_queryset(self):
        return models.Reviews.objects.filter(food_id = self.kwargs['food_pk'])

    def get_serializer_context(self):
        return {
            'request': self.request,
            'food_id': self.kwargs['food_pk']
        }
    

class CartViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin,  GenericViewSet):
    queryset = models.Cart.objects.prefetch_related('cart_items').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return models.CartItem.objects.filter(cart_id = self.kwargs['cart_pk']).select_related('food')

    # serializer_class = CartItemSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        else:
            return CartItemSerializer
        
    def get_serializer_context(self):
        return {
            'cart_id': self.kwargs['cart_pk']
        }
    

class UserViewSet(CreateModelMixin,RetrieveModelMixin, UpdateModelMixin,GenericViewSet):
    queryset = models.User.objects.all()
    serializer_class = UserSerializer


    # @action(detail=False,methods=['GET','PUT'])
    # (customer,created) = models.User.objects.get_or_create(user_id = request.user.id)
    # def me(self, request):
    #     if request.method == 'GET':
    #         serializer = UserSerializer(user)
    #         return Response(serializer.data)
    #     elif request.method == 'PUT':
    #         user = models.User.objects.get(user_id = request.user.id)
    #         serializer = UserSerializer(user,data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data)