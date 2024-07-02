from django.urls import path
from .views import get_top_products, get_product_details

urlpatterns = [
    path('categories/<str:category_name>/products/', get_top_products, name='get_top_products'),
    path('categories/<str:category_name>/products/<str:product_id>/', get_product_details, name='get_product_details'),
]
