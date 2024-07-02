from django.urls import path
from .views import calculate_average

urlpatterns = [
    path('numbers/<str:number_id>/', calculate_average, name='calculate_average')
]
