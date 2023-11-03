# Импорт библиотек
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import ApiUser, Warehouse, Product
from api.serializers import UserSerializer, WarehouseSerializer
from api.serializers import ProductSerializer


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = ApiUser.objects.all()
    http_method_names = ['post', 'get']
    serializer_class = UserSerializer

    authentication_classes = []
    permission_classes = []


class WarehouseModelViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.user_type == 'consumer':
            return Response({'detail': 'Consumers are not allowed \
                              to create warehouses'}, status=403)
        return super().create(request, *args, **kwargs)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.user_type == 'supplier':
            return Response({'detail': 'Suppliers are not \
                             allowed to create products'},
                            status=403)
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def ship_product(self, request, pk=None):
        user = request.user
        if user.user_type != 'supplier':
            return Response({'detail': 'Only suppliers can ship products'}, \
                            status=403)

        product = self.get_object()
        count = request.data.get('count')

        if count is None:
            return Response({'detail': 'Count parameter is required'}, \
                            status=400)

        try:
            product.ship(count)
        except ValueError as e:
            return Response({'detail': str(e)}, status=400)

        return Response({'detail': 'Product shipped successfully'})

    @action(detail=True, methods=['post'])
    def receive_product(self, request, pk=None):
        user = request.user
        if user.user_type != 'consumer':
            return Response({'detail': 'Only consumers can receive products'}, \
                            status=403)

        product = self.get_object()
        count = request.data.get('count')

        if count is None:
            return Response({'detail': 'Count parameter is required'}, \
                            status=400)

        product.receive(count)

        return Response({'detail': 'Product received successfully'})

