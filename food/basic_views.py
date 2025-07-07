# from . import models
# from django.db.models import Count
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Food, Collection
# from .serializers import FoodSerializer, CollectionSerializer
# from rest_framework import status
# from django.shortcuts import get_object_or_404

# # ADVANCED API CONCEPTS



# @api_view(['GET', 'POST'])
# def collection_list(request):
#     if request.method == 'POST':
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     elif request.method == 'GET':
#         collections = models.Collection.objects.annotate(total_foods=Count('food')).all()
#         serializer = CollectionSerializer(collections, many=True)
#         return Response(serializer.data)

# @api_view(['GET', 'PUT', 'DELETE'])
# def collection_detail(request, pk):
#     collection = get_object_or_404(Collection, pk=pk)
#     if request.method == 'GET': 
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True) 
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     elif request.method == 'DELETE':
#         if collection.food.count() > 0:
#             return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def food_list(request):
#     if request.method == 'POST':
#         serializer = FoodSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     elif request.method == 'GET':
#         products = models.Food.objects.select_related('collection').all()
#         serializer = FoodSerializer(products, many=True, context={'request': request})
#         return Response(serializer.data)


# @api_view(['GET', 'PUT', 'DELETE'])
# def food_detail(request, pk):
#     product = get_object_or_404(Food, pk=pk)
#     if request.method == 'GET':
#         serializer= FoodSerializer(product)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = FoodSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True) 
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     elif request.method == 'DELETE':
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Product cann  ot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
        
        