from rest_framework import generics, status
from .models import Bicycle, RentailHistory
from .serializers import BicycleSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from django.utils import timezone
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


def get_username_from_access_token(access_token):
    try:
        jwt_authentication = JWTAuthentication()
        validated_token = jwt_authentication.get_validated_token(access_token)
        user = jwt_authentication.get_user(validated_token)
        return user.username
    except:
        return None



class BicycleListAPIView(generics.ListAPIView):
    serializer_class = BicycleSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(description="""
        Запрос чтобы получить словарь свободных велосипедов.
        """,
                   summary="Словарь свободных велосипедов",
                   parameters=[
                       OpenApiParameter(
                           name="token",
                           type=str
                       )
                   ])
    def get_queryset(self):
        queryset = Bicycle.objects.filter(status=Bicycle.AVAILABLE)
        return queryset


class BicycleRentAPIView(generics.GenericAPIView):
    serializer_class = BicycleSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(description="""
            Запрос на аренду велосипедов.
            1 пользователь = 1 велосипед.
            """,
                   summary="Аренда велосипеда",
                   parameters=[
                       OpenApiParameter(
                           name="token",
                           type=str
                       ),
                       OpenApiParameter(
                           name="bicycle_id",
                           type=int
                       ),
                   ])
    def post(self, request):
        bicycle_id = request.data.get('bicycle_id')
        token = request.headers.get('Authorization').split(' ')[1]
        username = get_username_from_access_token(token)
        if not Bicycle.objects.filter(username=username).exists():
            try:
                bicycle = Bicycle.objects.get(id=bicycle_id, status=Bicycle.AVAILABLE)
            except Bicycle.DoesNotExist:
                return Response({'error': 'Неверный идентификатор велосипеда или велосипед недоступен.'}, status=status.HTTP_400_BAD_REQUEST)

            bicycle.status = Bicycle.RENTED
            bicycle.username = username
            bicycle.rent_start = timezone.now()
            bicycle.save()
            serializer = self.get_serializer(bicycle)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'status': 'error', 'error': 'Нельзя взять большего 1-го велосипеда'}, status=status.HTTP_400_BAD_REQUEST)


class ReturnBicycleView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(description="""
            Запрос чтобы сдать велосипедов.
            """,
                   summary="Вернуть велосипед",
                   parameters=[
                       OpenApiParameter(
                           name="token",
                           type=str
                       ),
                       OpenApiParameter(
                           name="bicycle_id",
                           type=int
                       ),
                   ])
    def post(self, request):
        bicycle_id = request.data.get('bicycle_id')
        token = request.headers.get('Authorization').split(' ')[1]
        username = get_username_from_access_token(token)
        try:
            bicycle = Bicycle.objects.get(id=bicycle_id, status=Bicycle.RENTED, username=username)
            rent_start_time = bicycle.rent_start
            rent_end_time = timezone.now()
            rental_duration = rent_end_time - rent_start_time
            rental_minute = float("{:.2f}".format(rental_duration.total_seconds() / 60))
            # calculate_rental_cost.delay(rental_minute, bicycle.price)
            rental_cost = rental_minute * bicycle.price
            bicycle.status = Bicycle.AVAILABLE
            data_history = {
                "bicycle_id": bicycle.id,
                "bicycle_name": bicycle.name,
                "username": username,
                "rental_cost": rental_cost,
                "rental_minute": rental_minute,
                "rent_start": rent_start_time,
                "rent_end": rent_end_time,
            }
            RentailHistory.objects.create(**data_history)
            bicycle.save()
        except Bicycle.DoesNotExist:
            return Response({'error': 'Bicycle not found or not rented by the current user'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'rental_cost': rental_cost, 'rental_minute': rental_minute}, status=status.HTTP_200_OK)

class RentalHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(description="""
            История аренды велосипедов пользователя.
            """,
                   summary="История аренды велосипедов",
                   parameters=[
                       OpenApiParameter(
                           name="token",
                           type=str
                       ),
                   ])
    def get(self, request):
        bicycles = RentailHistory.objects.filter(username=request.user.username)
        rental_history = []
        for bicycle in bicycles:
            rental_history.append({
                'id': bicycle.id,
                'bicycle_id': bicycle.bicycle_id,
                'bicycle_name': bicycle.bicycle_name,
                'username': bicycle.username,
                'rental_cost': bicycle.rental_cost,
                'rental_minute': bicycle.rental_minute,
                'rent_start': bicycle.rent_start,
                'rent_end': bicycle.rent_end,
            })
        return Response({'rental_history': rental_history})