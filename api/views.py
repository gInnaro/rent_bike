from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view
from drf_spectacular.types import OpenApiTypes
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

class Register_user(APIView):
    @extend_schema(description="""
    Запрос регистрации пользователей. 
    Для регистрации нужен никнейм, email, пароль.
    """,
                   summary="Создание новой учетной записи",
                   parameters=[
                       OpenApiParameter(
                           name="username",
                           type=str
                       ),
                       OpenApiParameter(
                           name="email",
                           type=OpenApiTypes.EMAIL
                       ),
                       OpenApiParameter(
                           name="password",
                           type=OpenApiTypes.PASSWORD
                       ),
                   ],
                   request=UserSerializer)
    def post(self, request):

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            refresh.payload.update({
                'user_id': user.id,
                'username': user.username
            })
            return Response({'success': 'Пользователь успешно зарегистрирован.', 'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_201_CREATED)
        return Response({'success': 'Пользователь с таким именем уже существует.'}, status=status.HTTP_400_BAD_REQUEST)
