from django.urls import path
from .views import CreateProductView, ProductView, DeleteProductView, UpdateProductView
urlpatterns = [
    path('createproduct/', CreateProductView.as_view(), name = 'createproduct' ),
    path('showproduct/', ProductView.as_view(), name = 'showproduct' ),
    path('deleteproduct/', DeleteProductView.as_view(), name = 'deleteproduct' ),
    path('updateproduct/', UpdateProductView.as_view(), name = 'updateproduct' )
]
