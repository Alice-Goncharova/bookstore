from rest_framework.routers import DefaultRouter
from django.urls import path
from api.views import UserModelViewSet, ProductViewSet, WarehouseModelViewSet

router = DefaultRouter()
router.register('users', UserModelViewSet)
router.register('product', ProductViewSet)
router.register('warehouse', WarehouseModelViewSet)



urlpatterns = [
    path('product/<int:pk>/ship/', ProductViewSet.as_view({'post': 'ship_product'}), name='product-ship'),
    path('product/<int:pk>/receive/', ProductViewSet.as_view({'post': 'receive_product'}), name='product-receive'),
]

urlpatterns.extend(router.urls)
