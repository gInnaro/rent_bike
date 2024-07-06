from django.urls import path
from .views import BicycleListAPIView, BicycleRentAPIView, ReturnBicycleView, RentalHistoryView

urlpatterns = [
    path('list/', BicycleListAPIView.as_view(), name='bicycle_list'),
    path('rent/', BicycleRentAPIView.as_view(), name='bicycle_rent'),
    path('return/', ReturnBicycleView.as_view(), name='return_bicycle'),
    path('rental_history/', RentalHistoryView.as_view(), name='rental_history'),
]